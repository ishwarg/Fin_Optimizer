using System;
using System.IO;

namespace Rocket_Simulator
{
    public class Functions
    {
        public static double lowerburn = 6.1;
        public static double upperburn = 12.76;
        public static double DR(double angle)
        {
            angle = (Math.PI) * angle / 180.0;
            return angle;
        }

        public static double ThrustInterpolator(double time, double[,] array,int stage)
        {
            double thrust = 0.0;
            int count = 0;

            if (time > lowerburn&&stage==1)
                return thrust;

            if (time > upperburn+lowerburn+Simulator.delay && stage == 2)
                return thrust;
            if (stage == 1)
            {
                while (array[count, 0] < time)
                {
                    count++;
                }

                if (count == 0)
                {
                    thrust = ((array[count, 1] - 0) / (array[count, 0] - 0))
                       * (time - 0) + 0;
                }
                else

                    thrust = ((array[count, 1] - array[count - 1, 1]) / (array[count, 0] - array[count - 1, 0]))
                            * (time - array[count - 1, 0]) + array[count - 1, 1];
            }

            else
            {
                time = time - lowerburn - Simulator.delay;
                while (array[count, 0] < time)
                {
                    count++;
                }

                if (count == 0)
                {
                    thrust = ((array[count, 1] - 0) / (array[count, 0] - 0))
                       * (time - 0) + 0;
                }
                else

                    thrust = ((array[count, 1] - array[count - 1, 1]) / (array[count, 0] - array[count - 1, 0]))
                            * (time - array[count - 1, 0]) + array[count - 1, 1];
            }

            return thrust;

        }

        public static void csvReader(string path, double[,] storage)
        {
            StreamReader var = new StreamReader(path);
            int i = 0;

            while (var.Peek() > -1)
            {
                string num;
                string temp1;
                string temp2;
                int index;
                num = var.ReadLine();
                index = num.IndexOf(',');
                temp1 = num.Substring(0, index);
                temp2 = num.Substring(index + 1, num.Length - 1 - index);
                storage[i, 0] = Convert.ToDouble(temp1);
                storage[i, 1] = Convert.ToDouble(temp2);
                
                i++;
                
            }
        }

        
        /*TO DO: AIR TEMP INTERPOLATOR
            Atmospheric Model
            Drag Coefficients


         */



    }
}