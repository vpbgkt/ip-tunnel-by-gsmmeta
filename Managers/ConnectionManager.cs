using System;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;

namespace IPTunnelGsmMeta.Managers
{
    /// <summary>
    /// Manages SSH tunnel connection lifecycle
    /// </summary>
    public class ConnectionManager
    {
        private Process? _sshProcess;
        private CancellationTokenSource? _monitorCts;
        private bool _isConnected = false;

        public event EventHandler<bool>? ConnectionStatusChanged;
        public event EventHandler<string>? LogMessage;

        public bool IsConnected => _isConnected;

        /// <summary>
        /// Start SSH tunnel connection
        /// </summary>
        public async Task<(bool success, string message)> ConnectAsync(string sshCommand)
        {
            if (_isConnected)
            {
                return (false, "Already connected");
            }

            try
            {
                // Parse the SSH command to extract parts
                var command = sshCommand.Trim();
                
                // PowerShell command to execute SSH
                var psCommand = $"& {command}";

                var processStartInfo = new ProcessStartInfo
                {
                    FileName = "powershell.exe",
                    Arguments = $"-NoProfile -NonInteractive -Command \"{psCommand}\"",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    RedirectStandardInput = true,
                    CreateNoWindow = true,
                    WindowStyle = ProcessWindowStyle.Hidden
                };

                _sshProcess = Process.Start(processStartInfo);
                
                if (_sshProcess == null)
                {
                    return (false, "Failed to start SSH process");
                }

                // Wait a moment to check if process started successfully
                await Task.Delay(1000);

                if (_sshProcess.HasExited)
                {
                    var error = await _sshProcess.StandardError.ReadToEndAsync();
                    return (false, $"SSH process exited immediately: {error}");
                }

                _isConnected = true;
                ConnectionStatusChanged?.Invoke(this, true);
                LogMessage?.Invoke(this, $"Connected successfully at {DateTime.Now:HH:mm:ss}");

                // Start monitoring the connection
                StartMonitoring();

                return (true, "Connection established successfully");
            }
            catch (Exception ex)
            {
                _isConnected = false;
                return (false, $"Connection failed: {ex.Message}");
            }
        }

        /// <summary>
        /// Disconnect SSH tunnel
        /// </summary>
        public async Task<(bool success, string message)> DisconnectAsync()
        {
            if (!_isConnected)
            {
                return (false, "Not connected");
            }

            try
            {
                // Stop monitoring
                StopMonitoring();

                if (_sshProcess != null && !_sshProcess.HasExited)
                {
                    // Try graceful shutdown first
                    _sshProcess.Kill(true);
                    await _sshProcess.WaitForExitAsync();
                }

                _sshProcess?.Dispose();
                _sshProcess = null;
                _isConnected = false;

                ConnectionStatusChanged?.Invoke(this, false);
                LogMessage?.Invoke(this, $"Disconnected at {DateTime.Now:HH:mm:ss}");

                return (true, "Disconnected successfully");
            }
            catch (Exception ex)
            {
                return (false, $"Error during disconnect: {ex.Message}");
            }
        }

        /// <summary>
        /// Start monitoring the connection status
        /// </summary>
        private void StartMonitoring()
        {
            _monitorCts = new CancellationTokenSource();
            var token = _monitorCts.Token;

            Task.Run(async () =>
            {
                while (!token.IsCancellationRequested && _isConnected)
                {
                    try
                    {
                        await Task.Delay(2000, token);

                        if (_sshProcess == null || _sshProcess.HasExited)
                        {
                            // Connection lost
                            _isConnected = false;
                            ConnectionStatusChanged?.Invoke(this, false);
                            LogMessage?.Invoke(this, $"Connection lost at {DateTime.Now:HH:mm:ss}");
                            break;
                        }
                    }
                    catch (TaskCanceledException)
                    {
                        break;
                    }
                }
            }, token);
        }

        /// <summary>
        /// Stop monitoring
        /// </summary>
        private void StopMonitoring()
        {
            _monitorCts?.Cancel();
            _monitorCts?.Dispose();
            _monitorCts = null;
        }

        /// <summary>
        /// Cleanup resources
        /// </summary>
        public void Dispose()
        {
            StopMonitoring();
            
            if (_sshProcess != null && !_sshProcess.HasExited)
            {
                try
                {
                    _sshProcess.Kill(true);
                }
                catch { }
            }
            
            _sshProcess?.Dispose();
        }

        /// <summary>
        /// Get connection uptime
        /// </summary>
        public TimeSpan GetUptime()
        {
            if (!_isConnected || _sshProcess == null)
            {
                return TimeSpan.Zero;
            }

            try
            {
                return DateTime.Now - _sshProcess.StartTime;
            }
            catch
            {
                return TimeSpan.Zero;
            }
        }
    }
}
