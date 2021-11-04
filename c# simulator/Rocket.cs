using System;
using System.Collections.Generic;
using System.Text;

namespace Rocket_Simulator
{
    class Rocket
    {
        public double thrust; public double mass; public double A; public double Ax; public double Ay; public double Az; public double V=0; public double Vx; public double Vy; public double Vz; public double D; public double Dx; public double Dy; public double altitude;
        public double partialD, partialV;

        public double Cg;
        public double phi, theta;
        public static double NoseCp=0.231;
        public static double NoseCn = 2;
        public static double Radius = 0.169 / 2;
        public static double Radius2 = 0.173 / 2;
        public static double Aref1 = Radius * Radius * Math.PI;
        public static double Aref2 = Radius2 * Radius2 * Math.PI;

        public double Ns, propmass;
        public double burn_time;
        public string thrust_curve;
        public double sound;
        public double length;
        public double time;


        public Rocket()
        {
         
        }
        public Rocket(string string1, double burn, double impulse, double propellant, double total_mass, double length)
        {
            thrust_curve = string1;
            burn_time = burn;
            Ns = impulse;
            propmass = propellant;
            mass = total_mass;
            this.length = length;
        }

       

        public double TotalCP(Fin Lower, Fin Upper, double Mach)
        {
            double CP = 0.0;
            

           CP= (NoseCn * NoseCp + Fin.finCP(Lower, Mach)*Fin.CN(Lower,Mach) + Fin.finCP(Upper, Mach) * Fin.CN(Upper,Mach)+cnt()*cpt()) / (Fin.CN(Lower,Mach)+ Fin.CN(Upper,Mach)+NoseCn+cnt());

            return CP;
        }
        public double TotalCP(Fin Upper, double Mach)
        {
            double CP = 0.0;


            CP = (NoseCn * NoseCp  + Fin.finCP(Upper, Mach) * Fin.CN(Upper, Mach)) / (Fin.CN(Upper, Mach) + NoseCn);

            return CP;
        }

       public double drag(Conditions conditions, int stage)
        {
            double force = 0;
            double cd = 0;
     

            if (stage == 1)
            {
                cd = Cd1(conditions);
                force = cd * 0.5 * V * V * conditions.rho * Aref2;
            }
            else
            {
                cd = Cd2(conditions);
                            force = cd * 0.5 * V * V * conditions.rho * Aref2;
            }
            
            


            return force;
            
        }

      
        public double Cd1(Conditions conditions)
        {
            double mach = Mach(conditions);
            double cd = 0;

            if (mach <= 0.042925)
            {
                cd = 0.233053 * Math.Pow(14.0063, -21.1859 * mach) + 0.481733;
            }

            if (mach > 0.042925 &&mach<0.899)
            {
                cd = 0.00956949 * Math.Pow(5.74899, 1.74902 * mach) +0.489959;
            }

            if (mach >= 0.899)
            {
                cd = 800.547 * Math.Pow(45.9163, -3.67846848432 * mach) + 0.640446941639;
            }

            return cd;
        }

        public double Cd2(Conditions conditions)
        {
            double mach = Mach(conditions);
            double cd = 0;

            if (mach <= 0.349)
            {
                cd = 0.00662570425938 * Math.Pow(3.42098298751,2.96986695803 * mach) + 0.339340944854;
            }

            if (mach > 0.349 && mach <= 0.91)
            {
               cd = 0.0228235809272 * Math.Pow(2.78129270714, 2.06810793328 * mach) + 0.315524806637;
            }

            if (mach > 0.91 && mach <= 1)
            {
                cd = 0.00559342361261 * Math.Pow(2.85814395849, 2.17394670594 * mach) + 0.427317691274;
            }

            if (mach > 1)
            {
                cd = 17.7798646006 * mach * mach * mach - 63.6607990234 * mach * mach + 75.2702063909 * mach - 28.9075455684;

            }

            return cd;
        }

            public double Mach(Conditions conditions)
        {


            // Earth  standard day
            double rgas = 1717;                /* ft2/sec2 R */
            double gama = 1.4;
            double alt = (altitude + conditions.launch_elevation) * 3.28084;
            double a0;
            double temp = 0.0;



            if (alt <= 36152)
            {           // Troposphere
                temp = 518.6 - 3.56 * alt / 1000;
            }
            if (alt >= 36152 && alt <= 82345)
            {   // Stratosphere
                temp = 389.98;
            }
            if (alt >= 82345 && alt <= 155348)
            {
                temp = 389.98 + 1.645 * (alt - 82345) / 1000;
            }
            if (alt >= 155348 && alt <= 175346)
            {
                temp = 508.788;
            }
            if (alt >= 175346 && alt <= 262448)
            {
                temp = 508.788 - 2.46888 * (alt - 175346) / 1000;
            }
            a0 = Math.Sqrt(gama * rgas * temp);  // feet /sec
            a0 = a0 * 60.0 / 88;
            sound = (a0 * 0.44704);


            return V/(a0 * 0.44704);


        }

        public double mdot(int stage)
        {
            double rate;

            if (stage == 1)
            {
                rate = 2.4;

            }

            //double exhaust = Ns / propmass;

            //rate = thrust / exhaust;

            else
                rate = 0.536;


            return rate;
        }

        public double totalmass(int stage)
        {
            double kgrams;
            kgrams = mass - mdot(stage)*Simulator.tstep;
            return kgrams;

        }

        public double netforce(double time,Conditions conditions, int stage, double firststagetime, Fin fin1, Fin fin2, Rocket rocket)
        {
            double force;
            double grav = 9.81 * Math.Cos(phi * Math.PI / 180)*mass;
            double drag = Drag.totaldrag(rocket, conditions, fin1, fin2, stage);

            if (time > burn_time && stage == 1)
            {
                thrust = 0;
                // force = -drag(conditions, stage) - grav;

              force=  -drag - grav;
            }

            else if (stage == 1 && time <= burn_time)
            {
                thrust = Functions.ThrustInterpolator(time, Simulator.LowerThrust,stage);
                // force = thrust - drag(conditions, stage) - grav;
                force = thrust - drag - grav;

            }
            else if (stage == 2 && time < burn_time + firststagetime) {
                thrust = Functions.ThrustInterpolator(time, Simulator.UpperThrust,stage);
                //force = thrust - drag(conditions, stage) - grav;
                force = thrust - drag - grav;
               
            }
            else {
                thrust = 0;
                force = -drag - grav;
            }

           
            return force;
        }
        public void avx(double time, Conditions conditions, int stage, double firststagetime, Rocket rocket, Fin fin1, Fin fin2)
        {
            double net = netforce(time, conditions, stage,firststagetime, fin1, fin2, rocket );

            A = net/ mass;
           
            partialV = A * Simulator.tstep;
            partialD = V * Simulator.tstep + 0.5 * Simulator.tstep * Simulator.tstep * A;
            V += partialV;
           

            
        }

        public double cnt()
        {
            double cn = 2 * (0.173 * 0.173 / 0.169 / 0.169 - 1);
            return 0;
        }

        public double cpt()
        {
            double cp = 1.92 + 0.005 / 3 * (1+(1-0.169/0.173)/(1- 0.169*0.169 / 0.173/0.173));
                return 0;

        }
    }
}
