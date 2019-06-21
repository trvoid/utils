using System;
using System.Linq;

namespace Utils
{
    public class ChartUtil
    {
        private static Tuple<int, int, double> GetLeadingDigits(double value, int leading_digit_count = 1)
        {
            if (leading_digit_count < 1)
            {
                throw new ArgumentOutOfRangeException($"leadingDigitCount({leading_digit_count}) is less than 1.");
            }

            int s = value >= 0 ? 1 : -1;
            double d = Math.Abs(value);
            int p = 0;

            if (d > 0)
            {
                double lb = Math.Pow(10, leading_digit_count - 1);
                double ub = Math.Pow(10, leading_digit_count);

                if (d >= lb)
                {
                    while (true)
                    {
                        if (d < ub)
                            break;
                        p += 1;
                        d /= 10;
                    }
                }
                else
                {
                    while (true)
                    {
                        if (d >= lb)
                            break;
                        p -= 1;
                        d *= 10;
                    }
                }
            }

            return new Tuple<int, int, double>(s, (int)d, Math.Pow(10, p));
        }

        private static Tuple<double, double> GetFloor(double value, int leading_digit_count = 1)
        {
            var ret = GetLeadingDigits(value, leading_digit_count);
            double _value = ret.Item1 * ret.Item2 * ret.Item3;
            if (value < 0 && _value != value)
            {
                _value -= ret.Item3;
            }
            return new Tuple<double, double>(_value, ret.Item3);
        }

        private static Tuple<double, double> GetCeil(double value, int leading_digit_count = 1)
        {
            var ret = GetLeadingDigits(value, leading_digit_count);
            double _value = ret.Item1 * ret.Item2 * ret.Item3;
            if (value > 0 && _value != value)
            {
                _value += ret.Item3;
            }
            return new Tuple<double, double>(_value, ret.Item3);
        }


        // Get an axis range for given values.
        // 
        // Example:
        //     For a value range (-41 ~ 35), axis range can be
        //         (-50 ~ 40) if leading digit count is 1, or
        //         (-42 ~ 36) if leading digit count is 2.
        public static Tuple<double, double, double> GetAxisRange(double[] values, int leading_digit_count = 1)
        {
            double min_value = values.Min();
            double max_value = values.Max();

            if (Math.Abs(max_value) >= Math.Abs(min_value))
            {
                var ret = GetCeil(max_value, leading_digit_count);
                double range_max = ret.Item1;
                double resolution = ret.Item2;

                double range_max_reduced = range_max / resolution;
                double range_min_reduced = range_max_reduced - 1;
                double min_value_reduced = min_value / resolution;

                while (true)
                {
                    if (range_min_reduced <= min_value_reduced)
                    {
                        break;
                    }
                    range_min_reduced -= 1;
                }

                double range_min = range_min_reduced * resolution;

                return new Tuple<double, double, double>(range_min, range_max, resolution);
            }
            else
            {
                var ret = GetFloor(min_value, leading_digit_count);
                double range_min = ret.Item1;
                double resolution = ret.Item2;

                double range_min_reduced = range_min / resolution;
                double range_max_reduced = range_min_reduced + 1;
                double max_value_reduced = max_value / resolution;

                while (true)
                {
                    if (range_max_reduced >= max_value_reduced)
                    {
                        break;
                    }
                    range_max_reduced += 1;
                }

                double range_max = range_max_reduced * resolution;

                return new Tuple<double, double, double>(range_min, range_max, resolution);
            }
        }

        public static double GetAxisInterval(double range_min, double range_max, double resolution)
        {
            double interval = resolution;
            double count = (range_max - range_min) / interval;

            while (count < 3 || count > 5)
            {
                if (count > 5)
                {
                    interval += resolution;
                }
                else if (count < 3)
                {
                    interval /= 10;
                }

                count = (range_max - range_min) / interval;
            }

            return interval;
        }
    }
}
