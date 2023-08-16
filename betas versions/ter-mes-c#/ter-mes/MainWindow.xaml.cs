using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Windows;
using System.Windows.Input;

namespace SimpleChatClient
{
    public partial class MainWindow : Window
    {
        private TcpClient clientSocket;
        private NetworkStream serverStream;
        private Thread receiveThread;
        private bool isConnected = false;
        private ManualResetEvent stopReceiveThread = new ManualResetEvent(false);

        public MainWindow()
        {
            InitializeComponent();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            serverIPTextBox.Text = "192.168.18.5";
            serverPortTextBox.Text = "12345";
            UpdateUI();
        }

        private void ConnectButton_Click(object sender, RoutedEventArgs e)
        {
            if (!isConnected)
            {
                string serverIP = serverIPTextBox.Text;
                int serverPort = int.Parse(serverPortTextBox.Text);

                try
                {
                    clientSocket = new TcpClient();
                    clientSocket.Connect(serverIP, serverPort);

                    serverStream = clientSocket.GetStream();

                    isConnected = true;
                    UpdateUI();

                    receiveThread = new Thread(ReceiveMessages);
                    receiveThread.Start();
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"No connection to server: {ex.Message}", "Connection Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }

        private void DisconnectButton_Click(object sender, RoutedEventArgs e)
        {
            if (isConnected)
            {
                Disconnect();
            }
        }

        private void SendButton_Click(object sender, RoutedEventArgs e)
        {
            SendMessage();
        }

        private void ReceiveMessages()
        {
            while (isConnected)
            {
                try
                {
                    byte[] buffer = new byte[1024];
                    int bytesRead = serverStream.Read(buffer, 0, buffer.Length);
                    string message = Encoding.UTF8.GetString(buffer, 0, bytesRead);

                    Dispatcher.Invoke(() =>
                    {
                        chatTextBox.AppendText(message + Environment.NewLine);
                    });
                }
                catch
                {
                    Disconnect();
                }
            }

            stopReceiveThread.Set(); // Signal that the thread has finished
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            Disconnect();
        }

        private void Disconnect()
        {
            if (isConnected)
            {
                isConnected = false;
                UpdateUI();

                try
                {
                    serverStream?.Close();
                    clientSocket?.Close();
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Error while disconnecting: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                }

                // Wait for the receiveThread to finish
                stopReceiveThread.WaitOne();
            }
        }

        private void UpdateUI()
        {
            connectButton.IsEnabled = !isConnected;
            disconnectButton.IsEnabled = isConnected;
            sendButton.IsEnabled = isConnected;
            messageTextBox.IsEnabled = isConnected;
        }

        private void ClearButton_Click(object sender, RoutedEventArgs e)
        {
            chatTextBox.Clear();
        }

        private void MessageTextBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                SendMessage();
                e.Handled = true;
            }
        }

        private void SendMessage()
        {
            if (isConnected && !string.IsNullOrWhiteSpace(messageTextBox.Text))
            {
                string message = $"{Environment.MachineName}: {messageTextBox.Text}";
                byte[] buffer = Encoding.UTF8.GetBytes(message);
                serverStream.Write(buffer, 0, buffer.Length);
                serverStream.Flush();
                messageTextBox.Clear();
            }
        }

        private void TextBox_TextChanged(object sender, System.Windows.Controls.TextChangedEventArgs e)
        {

        }
    }
}
