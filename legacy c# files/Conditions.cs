using System;
using System.Collections.Generic;
using System.Text;

namespace Rocket_Simulator
{
    class Conditions

    {
       
        public double rho;
        public double launch_elevation=1400;




        public Conditions()
        {

        }

        public void setConditions(Rocket rocket, double phi, double theta)
        {
            rocket.theta = theta;
            rocket.phi = phi;
            rho = 1.46090156792 * Math.Pow(0.999918544562,rocket.altitude+launch_elevation)-0.235174814257;
          
        }



        

        //    public double airpressure(Rocket rocket)
        //{
        //    return 101325 * Math.Pow((1 - 2.25577 * 0.00001 * (rocket.altitude+launch_elevation)), 5.25588);
        //}

    }
}
