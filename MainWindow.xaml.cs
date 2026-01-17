using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Windows;
using System.Windows.Media;
using System.Windows.Navigation;
using System.Windows.Threading;
using IPTunnelGsmMeta.Managers;

namespace IPTunnelGsmMeta;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window
{
    private readonly SshKeyManager _keyManager;
    private readonly ConfigManager _configManager;
    private readonly ConnectionManager _connectionManager;
    private readonly DispatcherTimer _uptimeTimer;
    private readonly List<string> _logs = new();
    
    private ConfigManager.AppConfig _config = new();

    public MainWindow()
    {
        InitializeComponent();
        
        _keyManager = new SshKeyManager();
        _configManager = new ConfigManager();
        _connectionManager = new ConnectionManager();
        
        _uptimeTimer = new DispatcherTimer
        {
            Interval = TimeSpan.FromSeconds(1)
        };
        _uptimeTimer.Tick += UptimeTimer_Tick;

        // Subscribe to connection events
        _connectionManager.ConnectionStatusChanged += OnConnectionStatusChanged;
        _connectionManager.LogMessage += OnLogMessage;

        Loaded += MainWindow_Loaded;
        Closing += MainWindow_Closing;
    }

    private async void MainWindow_Loaded(object sender, RoutedEventArgs e)
    {
        // Load configuration
        _config = await _configManager.LoadConfigAsync();
        
        // Update UI with config
        ServerCommandTextBox.Text = _config.ServerCommand;
        AutoConnectCheckbox.IsChecked = _config.AutoConnect;

        // Check SSH keys
        UpdateKeyStatus();

        Log("Application started");
        UpdateStatusBar("Ready");

        // Auto-connect if enabled
        if (_config.AutoConnect && !string.IsNullOrWhiteSpace(_config.ServerCommand))
        {
            await Task.Delay(1000); // Brief delay
            ToggleConnection();
        }
    }

    private void MainWindow_Closing(object? sender, System.ComponentModel.CancelEventArgs e)
    {
        _uptimeTimer.Stop();
        _connectionManager.Dispose();
    }

    private void UpdateKeyStatus()
    {
        if (_keyManager.KeysExist())
        {
            KeyStatusText.Text = $"✓ SSH keys found - {_keyManager.GetKeyInfo()}";
            KeyStatusText.Foreground = new SolidColorBrush(Colors.LightGreen);
            CopyKeyButton.IsEnabled = true;
            GenerateKeyButton.Content = "REGENERATE KEY";
        }
        else
        {
            KeyStatusText.Text = "No SSH keys found";
            KeyStatusText.Foreground = new SolidColorBrush(Colors.Gray);
            CopyKeyButton.IsEnabled = false;
            GenerateKeyButton.Content = "GENERATE KEY";
        }
    }

    private async void GenerateKeyButton_Click(object sender, RoutedEventArgs e)
    {
        GenerateKeyButton.IsEnabled = false;
        UpdateStatusBar("Generating SSH keys...");

        try
        {
            if (_keyManager.KeysExist())
            {
                var result = MessageBox.Show(
                    "SSH keys already exist. Do you want to delete them and generate new ones?",
                    "Confirm Regeneration",
                    MessageBoxButton.YesNo,
                    MessageBoxImage.Warning);

                if (result == MessageBoxResult.Yes)
                {
                    _keyManager.DeleteKeys();
                    Log("Existing SSH keys deleted");
                }
                else
                {
                    UpdateStatusBar("Key generation cancelled");
                    GenerateKeyButton.IsEnabled = true;
                    return;
                }
            }

            var (success, message) = await _keyManager.GenerateKeyAsync();
            
            if (success)
            {
                MessageBox.Show(message, "Success", MessageBoxButton.OK, MessageBoxImage.Information);
                Log("SSH keys generated successfully");
                UpdateKeyStatus();
                UpdateStatusBar("SSH keys generated");
            }
            else
            {
                MessageBox.Show(message, "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                Log($"ERROR: {message}");
                UpdateStatusBar("Key generation failed");
            }
        }
        finally
        {
            GenerateKeyButton.IsEnabled = true;
        }
    }

    private void CopyKeyButton_Click(object sender, RoutedEventArgs e)
    {
        if (_keyManager.CopyPublicKeyToClipboard())
        {
            MessageBox.Show("Public key copied to clipboard!", "Success", MessageBoxButton.OK, MessageBoxImage.Information);
            Log("Public key copied to clipboard");
            UpdateStatusBar("Public key copied");
        }
        else
        {
            MessageBox.Show("Failed to copy public key", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }
    }

    private async void SaveConfigButton_Click(object sender, RoutedEventArgs e)
    {
        var command = ServerCommandTextBox.Text.Trim();
        
        var (isValid, message) = ConfigManager.ValidateServerCommand(command);
        
        if (!isValid)
        {
            MessageBox.Show(message, "Invalid Command", MessageBoxButton.OK, MessageBoxImage.Warning);
            return;
        }

        _config.ServerCommand = command;
        var saved = await _configManager.SaveConfigAsync(_config);

        if (saved)
        {
            MessageBox.Show("Configuration saved successfully!", "Success", MessageBoxButton.OK, MessageBoxImage.Information);
            Log("Configuration saved");
            UpdateStatusBar("Configuration saved");
            
            // Switch to connection tab
            MainTabControl.SelectedIndex = 0;
        }
        else
        {
            MessageBox.Show("Failed to save configuration", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
        }
    }

    private void ToggleButton_Click(object sender, RoutedEventArgs e)
    {
        ToggleConnection();
    }

    private async void ToggleConnection()
    {
        if (_connectionManager.IsConnected)
        {
            // Disconnect
            ToggleButton.IsEnabled = false;
            var (success, message) = await _connectionManager.DisconnectAsync();
            ToggleButton.IsEnabled = true;

            if (!success)
            {
                MessageBox.Show(message, "Disconnect Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        else
        {
            // Connect
            if (string.IsNullOrWhiteSpace(_config.ServerCommand))
            {
                MessageBox.Show("Please configure server command first in the Setup tab", 
                    "Configuration Required", MessageBoxButton.OK, MessageBoxImage.Warning);
                MainTabControl.SelectedIndex = 1; // Switch to setup tab
                return;
            }

            ToggleButton.IsEnabled = false;
            var (success, message) = await _connectionManager.ConnectAsync(_config.ServerCommand);
            ToggleButton.IsEnabled = true;

            if (!success)
            {
                MessageBox.Show(message, "Connection Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
    }

    private void OnConnectionStatusChanged(object? sender, bool isConnected)
    {
        Dispatcher.Invoke(() =>
        {
            if (isConnected)
            {
                StatusIndicator.Fill = new SolidColorBrush(Colors.LightGreen);
                StatusText.Text = "Connected";
                ToggleButton.Content = "DISCONNECT";
                ToggleButton.Background = new SolidColorBrush(Color.FromRgb(220, 53, 69)); // Red
                UpdateStatusBar("Connected to server");
                _uptimeTimer.Start();
            }
            else
            {
                StatusIndicator.Fill = new SolidColorBrush(Colors.Gray);
                StatusText.Text = "Disconnected";
                ToggleButton.Content = "CONNECT";
                ToggleButton.ClearValue(BackgroundProperty);
                UpdateStatusBar("Disconnected");
                UptimeText.Text = "";
                _uptimeTimer.Stop();
            }
        });
    }

    private void OnLogMessage(object? sender, string message)
    {
        Log(message);
    }

    private void UptimeTimer_Tick(object? sender, EventArgs e)
    {
        var uptime = _connectionManager.GetUptime();
        if (uptime > TimeSpan.Zero)
        {
            UptimeText.Text = $"Uptime: {uptime:hh\\:mm\\:ss}";
        }
    }

    private async void AutoConnectCheckbox_Changed(object sender, RoutedEventArgs e)
    {
        _config.AutoConnect = AutoConnectCheckbox.IsChecked ?? false;
        await _configManager.SaveConfigAsync(_config);
        Log($"Auto-connect {(_config.AutoConnect ? "enabled" : "disabled")}");
    }

    private void ViewLogsButton_Click(object sender, RoutedEventArgs e)
    {
        var logsWindow = new LogsWindow(_logs);
        logsWindow.Owner = this;
        logsWindow.ShowDialog();
    }

    private void Hyperlink_RequestNavigate(object sender, RequestNavigateEventArgs e)
    {
        Process.Start(new ProcessStartInfo
        {
            FileName = e.Uri.AbsoluteUri,
            UseShellExecute = true
        });
        e.Handled = true;
    }

    private void Log(string message)
    {
        var timestamp = DateTime.Now.ToString("HH:mm:ss");
        var logEntry = $"[{timestamp}] {message}";
        _logs.Add(logEntry);
        
        // Keep last 500 entries
        if (_logs.Count > 500)
        {
            _logs.RemoveAt(0);
        }
    }

    private void UpdateStatusBar(string message)
    {
        StatusBarText.Text = message;
    }
}
