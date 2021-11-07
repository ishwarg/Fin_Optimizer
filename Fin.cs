using System;
using System.Collections.Generic;
using System.Text;

namespace Rocket_Simulator
{
    class Fin
    {
        public double AR, height, RC, TC, Sweep;
        public double Area, MAC, LE;
        public double MC;
        public double costau;
        public double t;

        //public Fin()
        //{

        //}

        public Fin(double h, double root, double tip, double s, double lead)
        {
            height = h;
            RC=root;
            TC=tip;
            Sweep=s;
            LE = lead;
            Area = (RC + TC) / 2 * height;
            AR = 2 * height * height / Area;
            t = TC / RC;
            MAC = RC * 2 / 3 * (1+t+t*t)/(1+t);
            MC = Math.Sqrt((height) * (height) + (Math.Abs(0.5 * RC - Sweep - 0.5 * TC)) * (Math.Abs(0.5 * RC - Sweep - 0.5 * TC)));
            costau = (height / MC);

        }

        public static double finCP(Fin fin, double Mach)
        {
            double[] poly = new double[6];
            calculatePoly(poly, fin);
            double CP = 0.0;
            double beta = Math.Sqrt(Math.Pow(Mach, 2) - 1);

            if (Mach < 0.5)
            {
                CP = fin.Sweep / 3 * (fin.RC + 2 * fin.TC) / (fin.RC + fin.TC) + 1 / 6 * (Math.Pow(fin.RC, 2) + Math.Pow(fin.TC, 2) + fin.RC * fin.TC) / (fin.RC + fin.TC);
                //CP = 0.25 * fin.MAC;
            }
            else if (Mach > 2.0)
            {

                CP = fin.MAC * (fin.AR * beta - 0.67) / (2 * fin.AR * beta - 1);

            }
            else
            {
                double x = 1.0;

                for (int i = 0; i < poly.Length; i++)
                {
                    CP += poly[i] * x;
                    x *= Mach;
                }
                CP = CP * fin.MAC;
            }



            // the reurn statement might be wrong



            return CP+ fin.LE;
            //  return CP + fin.LE+1/6*fin.height*(fin.RC-fin.TC)*(fin.Sweep+3*fin.LE)/fin.Area;

           // return fin.LE+CP + 1 / 6 * fin.height * (3 * fin.LE*(fin.RC+fin.TC)+fin.Sweep*(fin.RC+2*fin.TC))/fin.Area ;
        }

        //From Open Rocket
        public static void calculatePoly(double[] poly, Fin fin)
        {
            double denom = Math.Pow((1 - 3.4641 * fin.AR), 2); // common denominator

            poly[5] = (-1.58025 * (-0.728769 + fin.AR) * (-0.192105 + fin.AR)) / denom;
            poly[4] = (12.8395 * (-0.725688 + fin.AR) * (-0.19292 + fin.AR)) / denom;
            poly[3] = (-39.5062 * (-0.72074 + fin.AR) * (-0.194245 + fin.AR)) / denom;
            poly[2] = (55.3086 * (-0.711482 + fin.AR) * (-0.196772 + fin.AR)) / denom;
            poly[1] = (-31.6049 * (-0.705375 + fin.AR) * (-0.198476 + fin.AR)) / denom;
            poly[0] = (9.16049 * (-0.588838 + fin.AR) * (-0.20624 + fin.AR)) / denom;
        }
        public static double CN(Fin fin, double Mach)
        {
            double beta;
            if (Mach > 1)
            {
                beta = Math.Sqrt(Mach*Mach - 1);

            }
            else
            {
                beta = Math.Sqrt(1 - Mach*Mach);
            }

            //    return (1 + Rocket.Radius / (Rocket.Radius + fin.height)) * 4 * fin.height * fin.height / Rocket.Radius / Rocket.Radius /
            //(1 + Math.Sqrt(1 + (beta * fin.height * fin.height / fin.Area / fin.costau) * (beta * fin.height * fin.height / fin.Area / fin.costau)));

            // return (1+Rocket.Radius2/(Rocket.Radius2+fin.height))*(6.5*fin.height*fin.height/Rocket.Radius/Rocket.Radius) / (1+Math.Sqrt(1+(beta*fin.height*fin.height/fin.Area/fin.costau)* (beta * fin.height * fin.height / fin.Area / fin.costau)));


             return (1+Rocket.Radius/(fin.height+Rocket.Radius))* 4 * Math.PI * fin.height * fin.height / Rocket.Aref1 / (1+Math.Sqrt(1+(beta*fin.height*fin.height/fin.Area/fin.costau)* (beta * fin.height * fin.height / fin.Area / fin.costau)));
            //return 2 * Math.PI * pow2(fin.height) / (1 + Math.Sqrt(1 + (1 - pow2(Mach)) *
            //         pow2(pow2(fin.height) / (fin.Area * fin.costau)))) / Rocket.Aref;
        }
        public static double pow2(double input)
        {
            return input * input;
        }

    }

}