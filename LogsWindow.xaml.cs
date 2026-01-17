using System.Collections.Generic;
using System.Windows;

namespace IPTunnelGsmMeta
{
    public partial class LogsWindow : Window
    {
        private readonly List<string> _logs;

        public LogsWindow(List<string> logs)
        {
            InitializeComponent();
            _logs = logs;
            LoadLogs();
        }

        private void LoadLogs()
        {
            LogsTextBox.Text = string.Join("\n", _logs);
            LogsTextBox.ScrollToEnd();
        }

        private void CopyButton_Click(object sender, RoutedEventArgs e)
        {
            if (!string.IsNullOrEmpty(LogsTextBox.Text))
            {
                Clipboard.SetText(LogsTextBox.Text);
                MessageBox.Show("Logs copied to clipboard", "Success", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }

        private void ClearButton_Click(object sender, RoutedEventArgs e)
        {
            var result = MessageBox.Show(
                "Are you sure you want to clear all logs?",
                "Confirm Clear",
                MessageBoxButton.YesNo,
                MessageBoxImage.Question);

            if (result == MessageBoxResult.Yes)
            {
                _logs.Clear();
                LogsTextBox.Clear();
            }
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }
    }
}
