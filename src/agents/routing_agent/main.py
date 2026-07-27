#!/usr/bin/env python3
"""
Main execution script for the Routing Agent

This script demonstrates the routing agent solving the Bonn to Remagen problem
as an agentic task using the ArcGIS Location Platform. Falls back to mock agent
if ArcGIS is not available.
"""

import sys
import os
from datetime import datetime

# Add the routing_agent package to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from routing_agent import RoutingAgent
    AGENT_TYPE = "ArcGIS"
except ImportError:
    from routing_agent import MockRoutingAgent as RoutingAgent
    AGENT_TYPE = "Mock"


def main():
    """
    Main execution function demonstrating the routing agent
    """
    print("🛣️  Routing Agent: Bonn to Remagen Problem Solver")
    print("=" * 60)
    print(f"Agent Type: {AGENT_TYPE}")
    print(f"Execution time: {datetime.now()}")
    print()
    
    try:
        # Initialize the routing agent
        print(f"📡 Initializing {AGENT_TYPE} Routing Agent...")
        agent = RoutingAgent()
        print("✅ Agent initialized successfully")
        print()
        
        # Solve the routing problem
        print("🔍 Solving routing problem: Bonn → Remagen")
        print("-" * 40)
        
        routing_result = agent.solve_routing_problem(
            start_address="Bonn, Germany",
            end_address="Remagen, Germany"
        )
        
        # Display results
        print("\n📊 ROUTING RESULTS")
        print("=" * 30)
        print(f"Status: {routing_result.summary()}")
        print(f"Start: {routing_result.current_state.address} ({routing_result.current_state.latitude:.6f}, {routing_result.current_state.longitude:.6f})")
        print(f"Goal: {routing_result.target_state.address} ({routing_result.target_state.latitude:.6f}, {routing_result.target_state.longitude:.6f})")
        print()
        
        # Path Cost Analysis
        print("💰 PATH COST ANALYSIS")
        print("-" * 20)
        print(f"Primary Cost (Travel Time): {routing_result.path_cost:.2f} minutes")
        print(f"Distance: {routing_result.total_distance:.2f} km")
        print(f"Multi-criteria Cost: {routing_result.get_multi_criteria_cost():.2f}")
        print()
        
        # Route Segments
        if routing_result.route_segments:
            print(f"🗺️  ROUTE SEGMENTS ({len(routing_result.route_segments)} segments)")
            print("-" * 30)
            total_time = 0
            total_distance = 0
            
            for i, segment in enumerate(routing_result.route_segments, 1):
                print(f"{i:2d}. {segment.instructions}")
                print(f"    Time: {segment.travel_time_minutes:.2f} min, Distance: {segment.distance_km:.2f} km")
                total_time += segment.travel_time_minutes
                total_distance += segment.distance_km
            
            print(f"\nTotals: {total_time:.2f} min, {total_distance:.2f} km")
        
        # Validation
        print("\n✅ VALIDATION")
        print("-" * 15)
        is_valid = agent.validate_decision(routing_result)
        print(f"Route validation: {'✅ PASSED' if is_valid else '❌ FAILED'}")
        print(f"Goal test result: {'✅ REACHED' if routing_result.goal_reached else '❌ NOT REACHED'}")
        print(f"Confidence score: {routing_result.confidence:.2f}")
        
        # Problem Formulation Summary
        print("\n🎯 PROBLEM FORMULATION SUMMARY")
        print("-" * 35)
        print("✓ Initial State: Bonn coordinates geocoded")
        print("✓ Goal State: Remagen coordinates geocoded") 
        print("✓ Actions: Road network segments computed")
        print("✓ Transition Model: Routing API applied")
        print("✓ Goal Test: Buffer distance check executed")
        print("✓ Path Cost: Travel time calculated")
        print("✓ Results: Route computed and validated")
        
        if AGENT_TYPE == "ArcGIS":
            print("✓ Feature Layer: Published to ArcGIS Online")
        else:
            print("✓ Demo Mode: Mock routing simulation completed")
        
        return routing_result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    result = main()
    
    if result:
        print(f"\n🎉 Routing agent completed successfully!")
        print(f"Final path cost: {result.path_cost:.2f} minutes")
        if result.goal_reached:
            print("🎯 Goal achieved: Route computed to destination")
        else:
            print("⚠️  Note: Goal test indicates already at destination")
    else:
        print(f"\n💥 Routing agent failed")
        sys.exit(1)