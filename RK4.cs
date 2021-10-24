class RK4_Stepper
{
    private double time_step = 0;
    private double current_time = 0;
    private double current_position = 0;
    private double current_velocity = 0; 

    public RK4_Stepper()
    {
        time_step = 0.05;
    }

    public RK4_Stepper(double time_step)
    {
        this.time_step = time_step;
    }

    // acceleration = v' = f(t, v)
    private double get_acceleration(double time, double vel)
    {
        // TODO: Implement
    }
    
    // k1 = f(t, v)
    private double calculate_k1()
    {
        return get_acceleration(current_time, current_velocity);
    }

    // k2 = f(t + dt/2, v + dt*k1/2)
    private double calculate_k2()
    {
        return get_acceleration(current_time + time_step/2, current_velocity + time_step*k1/2);
    }
    
    // k3 = f(t + dt/2, v + dt*k2/2)
    private double calculate_k3()
    {
        return get_acceleration(current_time + time_step/2, current_velocity + time_step*k2/2);
    }

    // k4 = f(t + dt, v + h*k3)
    private double calculate_k4()
    {
        return get_acceleration(current_time + time_step, current_velocity + time_step*k3);
    }

    private double calculate_velocity_step()
    {
        k1 = calculate_k1();
        k2 = calculate_k2();
        k3 = calculate_k3();
        k4 = calculate_k4();
        return time_step * (k1 + k2 + k3 + k4) / 6;
    }

    private double calculate_position_step()
    {
        return current_velocity * time_step;
    }

    public void step()
    {
        current_velocity += calculate_velocity();
        current_position += calculate_position();
    }
}