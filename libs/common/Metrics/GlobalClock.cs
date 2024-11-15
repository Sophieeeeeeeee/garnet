using System.Diagnostics;

namespace Garnet.common
{
    public static class GlobalClock
    {
        // Static Stopwatch instance, started when the application initializes
        public static readonly Stopwatch Stopwatch = Stopwatch.StartNew();

        /// <summary>
        /// Get the current timestamp in ticks since the server started.
        /// </summary>
        public static long NowTicks => Stopwatch.ElapsedTicks;

        /// <summary>
        /// Get the current timestamp in milliseconds since the server started.
        /// </summary>
        public static double NowMilliseconds => Stopwatch.ElapsedMilliseconds;

        /// <summary>
        /// Get elapsed time in milliseconds from two timestamps.
        /// </summary>
        public static double ElapsedMilliseconds(long startTicks, long endTicks) =>
            (endTicks - startTicks) * 1000.0 / Stopwatch.Frequency;

        /// <summary>
        /// Get the frequency of the Stopwatch (ticks per second).
        /// </summary>
        public static long Frequency => Stopwatch.Frequency;
    }
}    
