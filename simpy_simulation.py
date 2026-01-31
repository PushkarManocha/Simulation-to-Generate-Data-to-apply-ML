import numpy as np
import pandas as pd
import simpy


def simulate_service_system(params, verbose=False):
    """Simulate a multi-server queue and return performance metrics."""

    def _safe_stats(sequence, reducer, empty_value=0.0):
        return reducer(sequence) if sequence else empty_value

    arrival_rate = params['arrival_rate']
    service_rate = params['service_rate']
    num_servers = params['num_servers']
    queue_capacity = params['queue_capacity']
    simulation_time = params.get('simulation_time', 1000)

    wait_times = []
    queue_lengths = []
    service_times = []
    served_count = 0
    rejected_count = 0

    rng = np.random.default_rng()
    env = simpy.Environment()
    server = simpy.Resource(env, capacity=num_servers)

    def customer(env, name, server, service_rate):
        """Process representing one arriving customer."""
        nonlocal served_count, rejected_count

        arrived_at = env.now

        if len(server.queue) >= queue_capacity:
            rejected_count += 1
            return

        with server.request() as request:
            yield request
            wait_times.append(env.now - arrived_at)

            service_duration = rng.exponential(1.0 / service_rate)
            yield env.timeout(service_duration)
            service_times.append(service_duration)
            served_count += 1

    def customer_generator(env, server, arrival_rate, service_rate):
        """Continuously inject customers into the system."""
        label = 0
        while True:
            inter_arrival = rng.exponential(1.0 / arrival_rate)
            yield env.timeout(inter_arrival)
            label += 1
            env.process(customer(env, f'c{label}', server, service_rate))
            queue_lengths.append(len(server.queue) + len(server.users))

    env.process(customer_generator(env, server, arrival_rate, service_rate))
    env.run(until=simulation_time)

    results = params.copy()
    results['avg_wait_time'] = _safe_stats(wait_times, np.mean)
    results['max_wait_time'] = _safe_stats(wait_times, np.max)
    results['std_wait_time'] = _safe_stats(wait_times, np.std)
    results['avg_queue_length'] = _safe_stats(queue_lengths, np.mean)
    results['max_queue_length'] = _safe_stats(queue_lengths, np.max)
    results['avg_service_time'] = _safe_stats(service_times, np.mean)

    results['customers_served'] = served_count
    results['customers_rejected'] = rejected_count
    total_customers = served_count + rejected_count
    results['rejection_rate'] = rejected_count / total_customers if total_customers else 0
    results['throughput'] = served_count / simulation_time

    if served_count:
        total_service_time = sum(service_times)
        total_server_time = simulation_time * num_servers
        results['utilization'] = (total_service_time / total_server_time) * 100
    else:
        results['utilization'] = 0

    acceptable_wait = 5.0
    results['service_level'] = (
        sum(1 for w in wait_times if w <= acceptable_wait) / len(wait_times) * 100
        if wait_times
        else 0
    )

    if verbose:
        print(f"Simulation complete: {served_count} served, {rejected_count} rejected")
        print(f"  Avg wait: {results['avg_wait_time']:.2f}, Utilization: {results['utilization']:.2f}%")

    return results


def generate_random_parameters():
    """Generate random simulation parameters within realistic bounds"""
    rng = np.random.default_rng()

    return {
        'arrival_rate': rng.uniform(1.0, 20.0),
        'service_rate': rng.uniform(0.5, 25.0),
        'num_servers': rng.integers(1, 11),
        'queue_capacity': rng.choice([5, 10, 15, 20, 25, 30, 40, 50]),
        'simulation_time': 1000,
    }


if __name__ == "__main__":
    print("Testing SimPy simulation framework...\n")
    
    # Test with random parameters
    test_params = generate_random_parameters()
    print("Test Parameters:")
    for k, v in test_params.items():
        print(f"  {k}: {v}")
    
    print("\nRunning simulation...")
    result = simulate_service_system(test_params, verbose=True)
    
    print("\nResults:")
    for k, v in result.items():
        if k not in test_params:
            if isinstance(v, float):
                print(f"  {k}: {v:.4f}")
            else:
                print(f"  {k}: {v}")
    
    print("\n" + "="*50)
    print("Generating 100 simulations for testing...")
    print("="*50)
    
    results = []
    for i in range(100):
        params = generate_random_parameters()
        result = simulate_service_system(params, verbose=False)
        results.append(result)
        if (i + 1) % 20 == 0:
            print(f"  {i+1} simulations complete...")
    
    df = pd.DataFrame(results)
    print(f"\nGenerated {len(df)} simulations")
    print(f"\nDataset shape: {df.shape}")
    print("\nSample statistics:")
    print(df[['avg_wait_time', 'utilization', 'throughput', 'service_level']].describe())
    
    print("\nSimPy simulation framework working as expected.")
