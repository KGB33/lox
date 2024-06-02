namespace dotlox
{
    public class Program
    {
        // Return code.
        enum ReturnValue : int
        {
            Ok = 0,
            UsageError = 1,
            ParsingError = 10,
            RuntimeError = 20,

        }
        static ReturnValue hadError = ReturnValue.Ok;
        public static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                // runRepl();
                run("""print "Hello, world!";""");
            }
            else if (args.Length == 1)
            {
                runFile(args[0]);
            }
            else
            {
                Console.WriteLine("Usage: dotlox [script]");
                hadError = ReturnValue.UsageError;
            }
        }

        ~Program()
        {
            Environment.ExitCode = (int)hadError;
        }


        private static void run(String src)
        {
            Scanner scanner = new Scanner(src);
            List<Token> tokens = scanner.scanTokens();

            foreach (Token t in tokens)
            {
                Console.WriteLine(t);
            }
        }

        private static void runRepl()
        {
            while (true)
            {
                Console.Write(">>> ");
                String line = Console.In.ReadLine() ?? "";
                if (line == "") break;
                run(line);
            }
        }

        private static void runFile(String path)
        {
            run(File.ReadAllText(path));
        }

        public static void error(int line, String message)
        {
            report(line, "", message);
        }

        private static void report(int line, String where, String message)
        {
            Console.Error.WriteLine($"[line: {line}] Error {where}: {message}");
            hadError = ReturnValue.RuntimeError;
        }
    }


}

