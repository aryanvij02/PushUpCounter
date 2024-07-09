import json
import sys

def analyze_joint_angles(file_path):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Initialize dictionaries to store min and max values for each joint
    min_angles = {}
    max_angles = {}

    # Analyze the data
    for frame in data:
        for joint, angle in frame.items():
            if isinstance(angle, (int, float)):  # Ensure the value is a number
                if joint not in min_angles or angle < min_angles[joint]:
                    min_angles[joint] = angle
                if joint not in max_angles or angle > max_angles[joint]:
                    max_angles[joint] = angle

    # Prepare the result
    result = {}
    for joint in min_angles.keys():
        max_angle = max_angles[joint]
        min_angle = min_angles[joint]
        
        # Calculate deadzones. But also ensures that deadzone_max is always greater than deadzone_min
        deadzone_max = max_angle * 0.7
        deadzone_min = min_angle * 1.3

        
        if deadzone_min > deadzone_max:
            deadzone_max = max_angle * 0.8
            deadzone_min = min_angle * 1.2

        if deadzone_min > deadzone_max:
            deadzone_max = max_angle * 0.9
            deadzone_min = min_angle * 1.1

        if deadzone_min > deadzone_max:
            deadzone_max = max_angle
            deadzone_min = min_angle
            

        result[joint] = {
            "max": round(max_angle, 2),
            "min": round(min_angle, 2),
            "deadzoneMax": round(deadzone_max, 2),
            "deadzoneMin": round(deadzone_min, 2)
        }

    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_json_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = analyze_joint_angles(file_path)

    # Print the result
    print(json.dumps(result, indent=2))

    # Save the result to a file
    with open('joint_angle_analysis_with_deadzones.json', 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()