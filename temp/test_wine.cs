using System;

class WineTest {
    static void Main() {
        Console.WriteLine("Wine .NET console test starting...");
        Console.WriteLine("OS Version: " + Environment.OSVersion);
        Console.WriteLine("Platform: " + Environment.OSVersion.Platform);
        Console.WriteLine("64-bit OS: " + Environment.Is64BitOperatingSystem);
        Console.WriteLine("CLR Version: " + Environment.Version);
        Console.WriteLine("Wine .NET test PASSED!");
    }
}
