using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace IPTunnelGsmMeta.Managers
{
    /// <summary>
    /// Manages SSH key generation, detection, and operations
    /// </summary>
    public class SshKeyManager
    {
        private readonly string _sshDir;
        private readonly string _privateKeyPath;
        private readonly string _publicKeyPath;

        public SshKeyManager()
        {
            _sshDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".ssh");
            _privateKeyPath = Path.Combine(_sshDir, "id_rsa");
            _publicKeyPath = Path.Combine(_sshDir, "id_rsa.pub");
        }

        /// <summary>
        /// Check if SSH keys exist
        /// </summary>
        public bool KeysExist()
        {
            return File.Exists(_privateKeyPath) && File.Exists(_publicKeyPath);
        }

        /// <summary>
        /// Generate new SSH key pair
        /// </summary>
        public async Task<(bool success, string message)> GenerateKeyAsync(string comment = "")
        {
            try
            {
                // Ensure .ssh directory exists
                Directory.CreateDirectory(_sshDir);

                if (KeysExist())
                {
                    return (false, "SSH keys already exist. Delete existing keys first if you want to regenerate.");
                }

                // Build ssh-keygen command
                var emailComment = string.IsNullOrEmpty(comment) ? "tech@gsmmeta.com" : comment;
                var arguments = $"-t rsa -b 2048 -f \"{_privateKeyPath}\" -N \"\" -C \"{emailComment}\"";

                var processStartInfo = new ProcessStartInfo
                {
                    FileName = "ssh-keygen",
                    Arguments = arguments,
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                };

                using var process = Process.Start(processStartInfo);
                if (process == null)
                {
                    return (false, "Failed to start ssh-keygen process");
                }

                var output = await process.StandardOutput.ReadToEndAsync();
                var error = await process.StandardError.ReadToEndAsync();
                await process.WaitForExitAsync();

                if (process.ExitCode == 0 && KeysExist())
                {
                    return (true, "SSH keys generated successfully!");
                }
                else
                {
                    return (false, $"Key generation failed: {error}");
                }
            }
            catch (Exception ex)
            {
                return (false, $"Error generating SSH keys: {ex.Message}");
            }
        }

        /// <summary>
        /// Get the public key content
        /// </summary>
        public string? GetPublicKey()
        {
            try
            {
                if (File.Exists(_publicKeyPath))
                {
                    return File.ReadAllText(_publicKeyPath).Trim();
                }
                return null;
            }
            catch
            {
                return null;
            }
        }

        /// <summary>
        /// Copy public key to clipboard
        /// </summary>
        public bool CopyPublicKeyToClipboard()
        {
            try
            {
                var publicKey = GetPublicKey();
                if (publicKey != null)
                {
                    Clipboard.SetText(publicKey);
                    return true;
                }
                return false;
            }
            catch
            {
                return false;
            }
        }

        /// <summary>
        /// Get key information
        /// </summary>
        public string GetKeyInfo()
        {
            if (!KeysExist())
            {
                return "No SSH keys found";
            }

            try
            {
                var fileInfo = new FileInfo(_privateKeyPath);
                return $"Key created: {fileInfo.CreationTime:yyyy-MM-dd HH:mm}";
            }
            catch
            {
                return "SSH keys exist";
            }
        }

        /// <summary>
        /// Delete existing SSH keys
        /// </summary>
        public (bool success, string message) DeleteKeys()
        {
            try
            {
                if (File.Exists(_privateKeyPath))
                {
                    File.Delete(_privateKeyPath);
                }
                if (File.Exists(_publicKeyPath))
                {
                    File.Delete(_publicKeyPath);
                }
                return (true, "SSH keys deleted successfully");
            }
            catch (Exception ex)
            {
                return (false, $"Error deleting keys: {ex.Message}");
            }
        }
    }
}
