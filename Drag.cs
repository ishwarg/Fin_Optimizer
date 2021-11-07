using System;
using System.Collections.Generic;
using System.Text;

namespace Rocket_Simulator
{
    class Drag
    {


        public Drag()
        {


        }

        public static double totaldrag(Rocket rocket, Conditions conditions, Fin fin1, Fin fin2, int stage)
        {

            double drag;
            drag = skin(conditions, rocket, stage, fin1, fin2) + pressure(conditions, rocket, stage) + finpressuredrag(rocket, conditions, fin1, fin2, stage) + basedrag(rocket, conditions);

            if (rocket.V < 1)
            {
                drag = skin(conditions, rocket, stage, fin1, fin2) + finpressuredrag(rocket, conditions, fin1, fin2, stage) + basedrag(rocket, conditions);
            }



            return drag;

        }

        public static double skin(Conditions conditions, Rocket rocket, int stage, Fin fin1, Fin fin2)
        {
            double[] data= new double[4];
            double sdrag = 0;
            double viscosity = 0.983686039133 * Math.Pow(1.00011284419, (rocket.altitude + conditions.launch_elevation)) + 0.480821017086;
            viscosity *= Math.Pow(10, -5);
            double Re;
            double Cf;
            double Rcrit;
            double Cfc;
            double Cd;
            double wetfin1;
            double wetfin2;
            double wetA = 179988.81 * 0.001 * 0.001 + 2 * Math.PI * Rocket.Radius * (1.895 - 0.5 + 4.02 - 2.22) + 2 * Math.PI * Rocket.Radius2 * 0.3 + 2 * Math.PI * Rocket.Radius * 0.3;
            double c1 = 1.0, c2 = 1.0;
            double mach = rocket.Mach(conditions);
            double roughness=10;

            if (stage == 1)
            {
                
                wetfin1 = 8 * fin1.Area + 4 * fin1.TC * 0.003;
                wetfin2 = 8 * fin2.Area + 4 * fin2.TC * 0.003;
                Re = rocket.V * 4.02 / viscosity;
                if (Re < 1e4)
                {
                    // Too low, constant
                    Cf = 1.48e-2;
                }
                else
                {
                    // Turbulent
                    Cf = 1.0 / pow2(1.50 * Math.Log(Re) - 5.6);
                }

                // Compressibility correction

                if (mach < 1.1)
                {
                    c1 = 1 - 0.1 * pow2(mach);
                }
                if (mach > 0.9)
                {
                    c2 = 1 / Math.Pow(1 + 0.15 * pow2(mach), 0.58);
                }
                // Applying continuously around Mach 1
                if (mach < 0.9)
                {
                    Cf *= c1;
                }
                else if (mach < 1.1)
                {
                    Cf *= c2 * (mach - 0.9) / 0.2 + c1 * (1.1 - mach) / 0.2;
                }
                else
                {
                    Cf *= c2;
                }



                // Roughness-limited value correction term
                double roughnessCorrection;
                if (mach < 0.9)
                {
                    roughnessCorrection = 1 - 0.1 * pow2(mach);
                }
                else if (mach > 1.1)
                {
                    roughnessCorrection = 1 / (1 + 0.18 * pow2(mach));
                }
                else
                {
                    c1 = 1 - 0.1 * pow2(0.9);
                    c2 = 1.0 / (1 + 0.18 * pow2(1.1));
                    roughnessCorrection = c2 * (mach - 0.9) / 0.2 + c1 * (1.1 - mach) / 0.2;
                }

                if (Cf < roughnessCorrection)
                {
                    Cf = 0.032 * Math.Pow(roughness * 0.000001 / rocket.length, 0.2) *
                         roughnessCorrection;
                }

            }

            else
            {
                
                wetfin1 = 0;
                wetfin2 = 8 * fin2.Area + 4 * fin2.TC * 0.003;
                wetA -= Math.PI * Rocket.Radius * (4.02 - 2.22);
                Re = rocket.V * 2.22 / viscosity;
                if (Re < 1e4)
                {
                    // Too low, constant
                    Cf = 1.48e-2;
                }
                else
                {
                    // Turbulent
                    Cf = 1.0 / pow2(1.50 * Math.Log(Re) - 5.6);
                }

                // Compressibility correction

                if (mach < 1.1)
                {
                    c1 = 1 - 0.1 * pow2(mach);
                }
                if (mach > 0.9)
                {
                    c2 = 1 / Math.Pow(1 + 0.15 * pow2(mach), 0.58);
                }
                // Applying continuously around Mach 1
                if (mach < 0.9)
                {
                    Cf *= c1;
                }
                else if (mach < 1.1)
                {
                    Cf *= c2 * (mach - 0.9) / 0.2 + c1 * (1.1 - mach) / 0.2;
                }
                else
                {
                    Cf *= c2;
                }



                // Roughness-limited value correction term
                double roughnessCorrection;
                if (mach < 0.9)
                {
                    roughnessCorrection = 1 - 0.1 * pow2(mach);
                }
                else if (mach > 1.1)
                {
                    roughnessCorrection = 1 / (1 + 0.18 * pow2(mach));
                }
                else
                {
                    c1 = 1 - 0.1 * pow2(0.9);
                    c2 = 1.0 / (1 + 0.18 * pow2(1.1));
                    roughnessCorrection = c2 * (mach - 0.9) / 0.2 + c1 * (1.1 - mach) / 0.2;
                }

                if (Re > 1e6 && Cf < roughnessCorrection)
                {
                    Cf = 0.032 * Math.Pow(roughness*0.000001 / rocket.length, 0.2) *
                        roughnessCorrection;
                }
            }


            //if (stage == 1)
            //{
            //    wetfin1 = 8 * fin1.Area + 4 * fin1.TC * 0.003;
            //    wetfin2 = 8 * fin2.Area + 4 * fin2.TC * 0.003;
            //    Re=rocket.V* 4.02 / viscosity;
            //    Rcrit = 51 * Math.Pow(0.5 * 0.000001 / 4.02, -1.039);
            //    if (Re < 10000)
            //        Cf = 0.0148;
            //    else if (Re >= 10000 && Re < Rcrit)
            //        Cf = 1 / (1.5 * Math.Log(Re) - 5.6) / (1.5 * Math.Log(Re) - 5.6);
            //    else
            //        Cf = 0.032 * Math.Pow(0.5 * 0.000001 / 4.02, 0.2);

            //}
            //else
            //{
            //    wetfin1 = 0;
            //    wetfin2 = 8 * fin2.Area + 4 * fin2.TC * 0.003;
            //    wetA -= Math.PI * Rocket.Radius * (4.02 - 2.22);
            //    Re = rocket.V * 2.22 / viscosity;
            //    Rcrit = 51 * Math.Pow(5 * 0.000001 / 2.22, -1.039);
            //    if (Re < 10000)
            //        Cf = 0.0148;
            //    else if (Re >= 10000 && Re < Rcrit)
            //        Cf = 1 / (1.5 * Math.Log(Re) - 5.6) / (1.5 * Math.Log(Re) - 5.6);
            //    else
            //        Cf = 0.032 * Math.Pow(5 * 0.000001 / 2.22, 0.2);
            //}

            //if (rocket.Mach(conditions) <= 0.9)
            //{
            //    Cfc = Cf * (1 - 0.1 * rocket.Mach(conditions) * rocket.Mach(conditions));
            //}
            //else
            //{
            //    Cfc = Cf / Math.Pow((1 + rocket.Mach(conditions) * rocket.Mach(conditions) * 0.15), 0.58);
            //    if (Cf / (1 + 0.18 * rocket.Mach(conditions) * rocket.Mach(conditions)) > Cfc)
            //        Cfc = Cf / (1 + 0.18 * rocket.Mach(conditions) * rocket.Mach(conditions));
            //}





            Cd = Cf * ((1 + 1 / 2 / (rocket.length / 2 / Rocket.Radius2)) * wetA + (1 + 2 * 0.003 / fin1.MAC) * wetfin1 + (1 + 2 * 0.003 / fin2.MAC) * wetfin2) / Rocket.Aref2;


            sdrag = 0.5 * Cd * conditions.rho * rocket.V * rocket.V * Rocket.Aref2;

            data[0] = rocket.Mach(conditions);
            data[1] = Re;
            data[2] = Cd;
            data[3] = Cd;

            //foreach (var item in data)
            //{
            //    Console.WriteLine(item);
            //}
          //  Console.WriteLine("{0:0.00}, {1:0.00}, {2:0.00}", rocket.V, rocket.altitude,Cd);
           
            return sdrag;
        }

        public static double pressure(Conditions conditions, Rocket rocket, int stage)

        {
            // if the drag functions dont work figure out how to scale the areas like it is done in the code. 

            double Cd = 0;
            double[] data = new double[4];
            double sinphi = Rocket.Radius / Math.Sqrt(Rocket.Radius * Rocket.Radius + 0.25);
            double c1, c2, c3, c4;
            c1 = 14.88;
            c2 = 54.18;
            c3 = 65.27;
            c4 = 25.8;


            double mul = (0.72 * Math.Pow(1 - 0.5, 2) + 0.82);

            // double cdMach1 = 2.1 * Math.Pow(sinphi, 2) + 0.6019 * sinphi;
            double minValue = c1 - c2 + c3 - c4;
            double cdMach0 = 0.8 * sinphi * sinphi;
            double minValue1 = c1 * 1.01 * 1.01 * 1.01 - c2 * 1.01 * 1.01 + c3 * 1.01 - c4;

            double minDeriv = (minValue1 - minValue) / 0.01;
            double a = minValue - cdMach0;
            double b = minDeriv / a;
            double drag;

            if (rocket.Mach(conditions) >= 0.8 && rocket.Mach(conditions) < 1.3)
            {
                Cd = c1 * rocket.Mach(conditions) * rocket.Mach(conditions) * rocket.Mach(conditions) - c2 * rocket.Mach(conditions) * rocket.Mach(conditions) + c3 * rocket.Mach(conditions) - c4;
                Cd *= mul;
            }
            else if (rocket.Mach(conditions) >= 1.3)
                Cd = mul * (2.1 * Math.Pow(sinphi, 2) + 0.5 * sinphi / Math.Sqrt(rocket.Mach(conditions) * rocket.Mach(conditions) - 1));
            else
                Cd = mul * (a * Math.Pow(rocket.Mach(conditions), b) + cdMach0);
            // Cd = 0.0;
          

            drag = 0.5 * Cd * conditions.rho * rocket.V * rocket.V * Rocket.Radius*Rocket.Radius*Math.PI;


            return drag;
        }

        public static double finpressuredrag(Rocket rocket, Conditions conditions, Fin fin1, Fin fin2, int stage)
        {
            double A1 = 4 * 0.003 * (fin1.height);
            double A2 = 4 * 0.003 * fin2.height;

            double drag;

            if (stage == 1)
            {

                drag = 0.5 * get_finp_drag(rocket, conditions, fin1) * rocket.V * rocket.V * conditions.rho * A1 + 0.5 * get_finp_drag(rocket, conditions, fin2) * rocket.V * rocket.V * conditions.rho * A2;

            }
            else

                drag = 0.5 * get_finp_drag(rocket, conditions, fin2) * rocket.V * rocket.V * conditions.rho * A2;


            return drag;
        }

        public static double basedrag(Rocket rocket, Conditions conditions)
        {

            return 0.5 * get_b_drag(rocket, conditions) * rocket.V * rocket.V * conditions.rho * Rocket.Aref2;
        }

        public static double get_finp_drag(Rocket rocket, Conditions conditions, Fin fin)
        {
            double CD_LE, CD_TE;
            double M = rocket.Mach(conditions);
            double cosGammaLead = Math.Cos(Math.Atan(fin.height / fin.Sweep));
            if (M < 0.9)
                CD_LE = Math.Pow((1 - M * M), -0.417) - 1;
            else if (M >= 0.9 && M < 1)
                CD_LE = 1 - 1.785 * (M - 0.9);
            else
                CD_LE = 1.214 - 0.502 / (Math.Pow(M, 2)) + 0.1095 / (Math.Pow(M, 4));

            CD_LE *= cosGammaLead * cosGammaLead;

            CD_TE = 0;   
            double pressure_drag = CD_LE + CD_TE;



            return pressure_drag;
        }


        public static double get_b_drag(Rocket rocket, Conditions conditions)
        {
            double base_drag;
            double M = rocket.Mach(conditions);

            if (M < 1)
                base_drag = 0.12 + 0.13 * Math.Pow(M, 2);
            else
                base_drag = 0.25 / M;

            return base_drag;
        }

        public static double pow2(double input)
        {
            return input * input;
        }

        public static double calculateStagnationCD(double m)
        {
            double pressure;
            if (m <= 1)
            {
                pressure = 1 + pow2(m) / 4 + pow2(pow2(m)) / 40;
            }
            else
            {
                pressure = 1.84 - 0.76 / pow2(m) + 0.166 / pow2(pow2(m)) + 0.035 / pow2(m * m * m);
            }
            return 0.85 * pressure;
        }


    }
}
