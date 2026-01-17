using System;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;

namespace IPTunnelGsmMeta.Managers
{
    /// <summary>
    /// Manages application configuration with JSON persistence
    /// </summary>
    public class ConfigManager
    {
        private readonly string _configDir;
        private readonly string _configFile;

        public ConfigManager()
        {
            _configDir = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
                "IPTunnelGsmMeta"
            );
            _configFile = Path.Combine(_configDir, "config.json");
        }

        /// <summary>
        /// Configuration model
        /// </summary>
        public class AppConfig
        {
            public string ServerCommand { get; set; } = string.Empty;
            public bool AutoConnect { get; set; } = false;
            public bool MinimizeToTray { get; set; } = false;
            public DateTime LastUpdated { get; set; } = DateTime.Now;
        }

        /// <summary>
        /// Load configuration from file
        /// </summary>
        public async Task<AppConfig> LoadConfigAsync()
        {
            try
            {
                if (!File.Exists(_configFile))
                {
                    return new AppConfig();
                }

                var json = await File.ReadAllTextAsync(_configFile);
                return JsonSerializer.Deserialize<AppConfig>(json) ?? new AppConfig();
            }
            catch
            {
                return new AppConfig();
            }
        }

        /// <summary>
        /// Save configuration to file
        /// </summary>
        public async Task<bool> SaveConfigAsync(AppConfig config)
        {
            try
            {
                // Ensure directory exists
                Directory.CreateDirectory(_configDir);

                config.LastUpdated = DateTime.Now;

                var options = new JsonSerializerOptions
                {
                    WriteIndented = true
                };

                var json = JsonSerializer.Serialize(config, options);
                await File.WriteAllTextAsync(_configFile, json);
                return true;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Validate server command format
        /// </summary>
        public static (bool isValid, string message) ValidateServerCommand(string command)
        {
            if (string.IsNullOrWhiteSpace(command))
            {
                return (false, "Server command cannot be empty");
            }

            command = command.Trim();

            // Check if command starts with ssh
            if (!command.StartsWith("ssh ", StringComparison.OrdinalIgnoreCase))
            {
                return (false, "Command must start with 'ssh'");
            }

            // Check for required flags
            if (!command.Contains("-R") && !command.Contains("-L"))
            {
                return (false, "Command must contain port forwarding (-R or -L)");
            }

            // Check for @ symbol (username@host)
            if (!command.Contains("@"))
            {
                return (false, "Command must contain username@host");
            }

            return (true, "Command is valid");
        }

        /// <summary>
        /// Get configuration directory path
        /// </summary>
        public string GetConfigDirectory()
        {
            return _configDir;
        }

        /// <summary>
        /// Check if configuration exists
        /// </summary>
        public bool ConfigExists()
        {
            return File.Exists(_configFile);
        }

        /// <summary>
        /// Delete configuration file
        /// </summary>
        public bool DeleteConfig()
        {
            try
            {
                if (File.Exists(_configFile))
                {
                    File.Delete(_configFile);
                }
                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}
