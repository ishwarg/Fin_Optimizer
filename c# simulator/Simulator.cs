using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;



namespace Rocket_Simulator
{
    class Simulator
    {
        public static double[,] LowerThrust = new double[15, 2];
        public static double[,] UpperThrust = new double[22, 2];
        public static double delay = 4;
        public static string path1 = "C:/Users/ishwa/Downloads/Cesaroni_21062O3400-P.csv";
        public static string path2 = "C:/Users/ishwa/Downloads/Cesaroni_10133M795-P.csv";
        public static string path3 = "C:/Users/ishwa/Downloads/Output.csv";




        public static double tstep = 0.01;




        static void Main(string[] args)
        {

            //sim();
            //simbutwithcd();

            testing();

           



        }

        public static void testing()
        {
            //double time = 0.0;


            Rocket first_stage = new Rocket(path1, 6.1, 21041.0, 11.272, 54.326, 4.02);
            Rocket second_stage = new Rocket(path2, 12.76, 10133, 4.892, 26.072, 2.22);
            Fin lowerstage = new Fin(0.166, 0.3, 0.06, 0.22, 3.715);
            Fin upperstage = new Fin(0.16, 0.3, 0.04, 0.24, 1.9);
            Conditions sim1 = new Conditions();
            double dummy;


            //while (true)
            //{
            //    second_stage.V = Convert.ToDouble(Console.ReadLine());
            //    second_stage.altitude = Convert.ToDouble(Console.ReadLine());
            //    sim1.setConditions(second_stage, 5, 0);
            //    Console.Clear();
            //    Console.WriteLine(Drag.skin(sim1,second_stage,2,lowerstage,upperstage)/second_stage.V/second_stage.V/0.5/sim1.rho/Rocket.Aref);
            //    Console.WriteLine(Drag.pressure(sim1, second_stage, 2) / second_stage.V / second_stage.V / 0.5 / sim1.rho / Rocket.Aref);
            //    Console.WriteLine(Drag.finpressuredrag(second_stage,sim1, lowerstage,upperstage,2)/ second_stage.V / second_stage.V / 0.5 / sim1.rho / Rocket.Aref);
            //    Console.WriteLine(Drag.basedrag(second_stage,sim1) / second_stage.V / second_stage.V / 0.5 / sim1.rho / Rocket.Aref);
            //    Console.WriteLine(Drag.totaldrag(second_stage,sim1, lowerstage,upperstage,2) / second_stage.V / second_stage.V / 0.5 / sim1.rho / Rocket.Aref);
            //}


            //Console.WriteLine(first_stage.TotalCP(lowerstage,upperstage,0.125)); 
            Fin testfin=new Fin(0.25, 0.3, 0.05, 0.025, 0.5);
            Console.WriteLine((0.231*2+Fin.finCP(testfin,0.13)*2*Fin.CN(testfin,0.13))/(2+ 2*Fin.CN(testfin, 0.13)));






        }

        public static void sim()
        {
            double time = 0.0;


            Rocket first_stage = new Rocket(path1, 6.1, 21041.0, 11.272, 54.326, 4.02);
            Rocket second_stage = new Rocket(path2, 12.76, 10133, 4.892, 26.072, 2.22);
            Fin lowerstage = new Fin(0.166, 0.3, 0.06, 0.22, 3.72);
            Fin upperstage = new Fin(0.16, 0.3, 0.24, 0.04, 1.9);
            Conditions sim1 = new Conditions();
            //System.IO.File.WriteAllText(path3, string.Empty);

            //using (StreamWriter writer = new StreamWriter(path3, true))
            //{
            //    writer.WriteLine("time,thrust,drag,coeffcient,A,Az,V,Vz,Altitude");
            //}

            Functions.csvReader(path1, LowerThrust);
            Functions.csvReader(path2, UpperThrust);

            sim1.setConditions(first_stage, 5, 0);



            while (time <= first_stage.burn_time)
            {
                first_stage.avx(time, sim1, 1, time, first_stage, lowerstage, upperstage);
                first_stage.Az = first_stage.A * Math.Cos(first_stage.phi * Math.PI / 180);
                first_stage.altitude += first_stage.partialD * Math.Cos(first_stage.phi * Math.PI / 180);
                first_stage.mass = first_stage.totalmass(1);
                sim1.setConditions(first_stage, 5, 0);
                first_stage.Vz = first_stage.V * Math.Cos(first_stage.phi * Math.PI / 180);
                first_stage.time = time;
                printstats(first_stage,time,sim1,1);


                //using (StreamWriter writer = new StreamWriter(path3, true))
                //{
                //    writer.WriteLine("{0},{1},{2},{3},{4},{5},{6},{7},{8}", time, first_stage.thrust, first_stage.drag(sim1, 1), first_stage.Cd1(sim1), first_stage.A, first_stage.Az, first_stage.V, first_stage.Vz, first_stage.altitude);
                //}

                time += tstep;

            }
            while (time <= first_stage.burn_time+delay)
            {
                first_stage.avx(time, sim1, 1, time, first_stage, lowerstage, upperstage);
                first_stage.Az = first_stage.A * Math.Cos(first_stage.phi * Math.PI / 180);
                first_stage.altitude += first_stage.partialD * Math.Cos(first_stage.phi * Math.PI / 180);
                
                sim1.setConditions(first_stage, 5, 0);
                first_stage.Vz = first_stage.V * Math.Cos(first_stage.phi * Math.PI / 180);
                first_stage.time = time;
                printstats(first_stage, time, sim1, 1);

                //using (StreamWriter writer = new StreamWriter(path3, true))
                //{
                //    writer.WriteLine("{0},{1},{2},{3},{4},{5},{6},{7},{8}", time, first_stage.thrust, first_stage.drag(sim1, 1), first_stage.Cd1(sim1), first_stage.A, first_stage.Az, first_stage.V, first_stage.Vz, first_stage.altitude);
                //}

                time += tstep;

            }


            second_stage.altitude = first_stage.altitude;
            sim1.setConditions(second_stage, 5, 0);
            second_stage.V = first_stage.V;
            second_stage.Vz = second_stage.V * Math.Cos(second_stage.phi * Math.PI / 180);
            double current = time;

            while (time < current + second_stage.burn_time)
            {
                second_stage.avx(time, sim1, 2, first_stage.burn_time + delay, second_stage, lowerstage, upperstage);
                second_stage.Az = second_stage.A * Math.Cos(second_stage.phi * Math.PI / 180);
                second_stage.Vz = second_stage.V * Math.Cos(second_stage.phi * Math.PI / 180);
                second_stage.altitude += second_stage.partialD * Math.Cos(second_stage.phi * Math.PI / 180);
                second_stage.mass = second_stage.totalmass(2);
                sim1.setConditions(second_stage, 5, 0);
                second_stage.time = time;
                time += tstep;
                printstats(second_stage, time, sim1, 2);
            }

            
            while (second_stage.Vz > 0)
            {
                
                second_stage.avx(time, sim1, 2, first_stage.burn_time + delay, second_stage, lowerstage, upperstage);
                second_stage.Az = second_stage.A * Math.Cos(second_stage.phi * Math.PI / 180);
                second_stage.Vz = second_stage.V * Math.Cos(second_stage.phi * Math.PI / 180);
                second_stage.altitude += second_stage.partialD * Math.Cos(second_stage.phi * Math.PI / 180);
                //second_stage.mass = second_stage.totalmass(2);
                sim1.setConditions(second_stage, 5, 0);
                second_stage.time = time;
                time += tstep;
                printstats(second_stage, time, sim1, 2);
                //using (StreamWriter writer = new StreamWriter(path3, true))
                //{
                //    writer.WriteLine("{0},{1},{2},{3},{4},{5},{6},{7},{8}", time, second_stage.thrust, second_stage.drag(sim1, 1), second_stage.Cd2(sim1), second_stage.A, second_stage.Az, second_stage.V, second_stage.Vz, second_stage.altitude);
                //}

            }

            Console.WriteLine("{0:0.00}", second_stage.altitude * 3.281);
            Console.WriteLine(time);


        }

        public static void simbutwithcd()
        {
            double time = 0.0;


            Rocket first_stage = new Rocket(path1, 6.1, 21041.0, 11.272, 54.326, 4.02);
            Rocket second_stage = new Rocket(path2, 12.76, 10133, 4.892, 26.072, 2.22);
            Fin lowerstage = new Fin(0.16, 0.3, 0.06, 0.22, 3.72);
            Fin upperstage = new Fin(0.166, 0.3, 0.24, 0.04, 1.9);
            Conditions sim1 = new Conditions();
            System.IO.File.WriteAllText(path3, string.Empty);

            using (StreamWriter writer = new StreamWriter(path3, true))
            {
                writer.WriteLine("time, Mach,pressure");
            }

            Functions.csvReader(path1, LowerThrust);
            Functions.csvReader(path2, UpperThrust);

            sim1.setConditions(first_stage, 5, 0);



            while (time <= first_stage.burn_time + delay)
            {
                Console.WriteLine("{0:0.00},{1:0.00} ", time,Drag.totaldrag(first_stage,sim1,lowerstage,upperstage,1)/0.5/first_stage.V/first_stage.V/sim1.rho/Rocket.Aref2);
                first_stage.avx(time, sim1, 1, time, first_stage, lowerstage, upperstage);
                first_stage.Az = first_stage.A * Math.Cos(first_stage.phi * Math.PI / 180);
                first_stage.altitude += first_stage.partialD * Math.Cos(first_stage.phi * Math.PI / 180);
                first_stage.mass = first_stage.totalmass(1);
                sim1.setConditions(first_stage, 5, 0);
                first_stage.Vz = first_stage.V * Math.Cos(first_stage.phi * Math.PI / 180);

                //using (StreamWriter writer = new StreamWriter(path3, true))
                //{
                //    writer.WriteLine("{0},{1},{2}",time, first_stage.Mach(sim1), (Drag.pressure(sim1, first_stage,1)+ Drag.finpressuredrag(first_stage,sim1, lowerstage,upperstage, 1))/first_stage.V/first_stage.V/0.5/sim1.rho/Rocket.Aref);
                //}

                time += tstep;

            }
            second_stage.altitude = first_stage.altitude;
            sim1.setConditions(second_stage, 5, 0);
            second_stage.V = first_stage.V;
            second_stage.Vz = second_stage.V * Math.Cos(second_stage.phi * Math.PI / 180);

            while (second_stage.Vz > 0)
            {
                Console.WriteLine("{0:0.00},{1:0.00} ", time, Drag.totaldrag(second_stage, sim1, lowerstage, upperstage, 2)/0.5/second_stage.V/second_stage.V/sim1.rho/Rocket.Aref2);
                second_stage.avx(time, sim1, 2, first_stage.burn_time + delay, second_stage, lowerstage, upperstage);
                second_stage.Az = second_stage.A * Math.Cos(second_stage.phi * Math.PI / 180);
                second_stage.Vz = second_stage.V * Math.Cos(second_stage.phi * Math.PI / 180);
                second_stage.altitude += second_stage.partialD * Math.Cos(second_stage.phi * Math.PI / 180);
                second_stage.mass = second_stage.totalmass(2);
                sim1.setConditions(second_stage, 5, 0);
                time += tstep;
                
                

                //using (StreamWriter writer = new StreamWriter(path3, true))
                //{
                //    writer.WriteLine("{0},{1},{2}",time, second_stage.Mach(sim1), (Drag.pressure(sim1, first_stage, 1)+Drag.finpressuredrag(second_stage, sim1, lowerstage, upperstage, 2)) / second_stage.V / second_stage.V / 0.5 / sim1.rho/Rocket.Aref);
                //}

            }

            Console.WriteLine("{0:0.00}", second_stage.altitude * 3.281);
            Console.WriteLine(time);
        }

        public static void printstats(Rocket rocket, double time, Conditions conditions, int stage)
        {
            Console.WriteLine("{0:0.00},{1:0.00},{2:0.00},{3:0.00}", time,rocket.V,rocket.altitude,Drag.pressure(conditions,rocket,stage)/rocket.V/rocket.V/0.5/conditions.rho/Rocket.Aref2);
        }


    }








}


