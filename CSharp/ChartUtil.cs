using System;
using System.Linq;

namespace Utils
{
    public class ChartUtil
    {
        private static Tuple<int, int> GetLeadingDigits(double value, int leading_digit_count = 1)
        {
            if (value == 0)
            {
                return new Tuple<int, int>(0, 0);
            }

            double d = value;
            int p = 0;

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

            return new Tuple<int, int>((int)d, p);
        }

        private static Tuple<double, int> GetCeil(double value, int leading_digit_count = 1)
        {
            var ret = GetLeadingDigits(value, leading_digit_count);
            double _value = ret.Item1 * Math.Pow(10, ret.Item2);
            if (_value != value)
            {
                _value += Math.Pow(10, ret.Item2);
            }
            return new Tuple<double, int>(_value, ret.Item2);
        }

        public static Tuple<double, double> GetAxisRange(double[] values, int leading_digit_count = 1)
        {
            double min_value = values.Min();
            double max_value = values.Max();

            var ret = GetCeil(max_value, leading_digit_count);
            double range_max = ret.Item1;
            double resolution = Math.Pow(10, ret.Item2);

            if (range_max == max_value)
            {
                range_max += resolution;
            }

            double range_max_reduced = range_max / resolution;
            double range_min_reduced = range_max_reduced - 1;
            double min_value_reduced = min_value / resolution;

            while (true)
            {
                if (range_min_reduced < min_value_reduced)
                {
                    break;
                }
                range_min_reduced -= 1;
            }

            double range_min = range_min_reduced * resolution;

            return new Tuple<double, double>(range_min, range_max);
        }
    }
}
