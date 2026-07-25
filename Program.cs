using System;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Text;
using System.Threading;

namespace HamiltonJacobiEngine
{
    class Program
    {
        static void Main(string[] args)
        {
            int port = 8080;
            int customPort;
            if (args.Length > 0 && int.TryParse(args[0], out customPort))
            {
                port = customPort;
            }

            try
            {
                Console.Title = "Hamilton-Jacobi Equation Solution Server - Scopus Q1 Top 1%";
                Console.Clear();
                Console.ForegroundColor = ConsoleColor.Yellow;
            }
            catch { }

            Console.WriteLine("==============================================================");
            Console.WriteLine("    ⚡ HAMILTON-JACOBI EQUATION SOLUTION SERVER (SCOPUS Q1)");
            Console.WriteLine("    Karya: Samuel Hasiholan Omega, S. Tr. T.");
            Console.WriteLine("==============================================================");
            try
            {
                Console.ResetColor();
            }
            catch { }

            Console.WriteLine(" Server berhasil dijalankan!");
            Console.WriteLine(" Silakan akses aplikasi melalui peramban (browser) di:");
            try
            {
                Console.ForegroundColor = ConsoleColor.Green;
            }
            catch { }
            Console.WriteLine(" --> http://localhost:" + port + "/");
            try
            {
                Console.ResetColor();
            }
            catch { }
            Console.WriteLine(" [SCOPUS Q1 ENGINE] Hamilton-Jacobi PDE Solver & HJB Control Active.");
            Console.WriteLine("==============================================================");
            Console.WriteLine(" Membuka peramban otomatis...");

            try
            {
                Process.Start("http://localhost:" + port + "/");
            }
            catch
            {
                try
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = "cmd",
                        Arguments = "/c start http://localhost:" + port + "/",
                        CreateNoWindow = true,
                        UseShellExecute = false
                    });
                }
                catch { }
            }

            StartHttpServer(port);
        }

        static void StartHttpServer(int port)
        {
            try
            {
                HttpListener listener = new HttpListener();
                listener.Prefixes.Add("http://localhost:" + port + "/");
                listener.Prefixes.Add("http://127.0.0.1:" + port + "/");
                listener.Start();

                while (true)
                {
                    HttpListenerContext context = listener.GetContext();
                    ThreadPool.QueueUserWorkItem((state) => HandleRequest(context));
                }
            }
            catch (Exception ex)
            {
                Console.ForegroundColor = ConsoleColor.Red;
                Console.WriteLine("[ERROR] HttpListener exception: " + ex.Message);
                Console.ResetColor();
            }
        }

        static void HandleRequest(HttpListenerContext context)
        {
            HttpListenerRequest request = context.Request;
            HttpListenerResponse response = context.Response;

            string rawUrl = request.Url.AbsolutePath;
            if (rawUrl == "/") rawUrl = "/index.html";

            string filePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, rawUrl.TrimStart('/'));

            if (!File.Exists(filePath))
            {
                response.StatusCode = 404;
                byte[] notFoundBytes = Encoding.UTF8.GetBytes("404 Not Found - Hamilton-Jacobi Equation Solution Server");
                response.OutputStream.Write(notFoundBytes, 0, notFoundBytes.Length);
                response.Close();
                return;
            }

            try
            {
                byte[] content = File.ReadAllBytes(filePath);
                response.ContentType = GetContentType(Path.GetExtension(filePath));
                response.ContentLength64 = content.Length;
                response.OutputStream.Write(content, 0, content.Length);
            }
            catch (Exception ex)
            {
                response.StatusCode = 500;
                byte[] errBytes = Encoding.UTF8.GetBytes("500 Server Error: " + ex.Message);
                response.OutputStream.Write(errBytes, 0, errBytes.Length);
            }
            finally
            {
                response.Close();
            }
        }

        static string GetContentType(string extension)
        {
            switch (extension.ToLower())
            {
                case ".html": return "text/html; charset=utf-8";
                case ".css": return "text/css";
                case ".js": return "application/javascript";
                case ".json": return "application/json";
                case ".png": return "image/png";
                case ".jpg": return "image/jpeg";
                case ".svg": return "image/svg+xml";
                default: return "application/octet-stream";
            }
        }
    }
}
