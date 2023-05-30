import openai
import re
import time

openai.api_key = "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"

# Define the code file path
code_file_path = r'C:\Users\leduc\OneDrive\Desktop\vulnerabilityLib.c' # Replace with 'benignLib' for testing codes in benign library
                                                                                    

# Read the code file
with open(code_file_path, "r") as file:
    code = file.read()

# Split the code into individual functions
function_regex = r"\/\*funcstart\*\/(.*?)\/\*funcend\*\/"
functions = re.findall(function_regex, code, re.DOTALL)

# Initialize variables to store the metrics
total_functions = len(functions)
vulnerable_functions = 0

# Create a file to store the results
result_file_path = r'C:\Users\leduc\OneDrive\Desktop\Vulnerability_results.txt'   # Change this to 'Benign_results' when testing codes in benign library
result_file = open(result_file_path, "w")
result_file.write("Vulnerability library code that are vulnerable: \n\n")       # Change this to 'Benign' when testing codes in benign library

# Iterate over each function
for i, func in enumerate(functions):
    # Generate the prompt by removing the function name and comments
    chat_input = "Is the following code vulnerable to buffer overflow? Answer starts with Y if it is vulnerable or with N if it is not vulnerable: " + func

    # Send the user message to the API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": chat_input}
        ],
    )

    # Extract the model's reply
    reply = response.choices[0].message.content
    print(reply)
    print(response)

    # Determine if the code is vulnerable based on the response
    is_vulnerable = reply.startswith('Y')

    # Count the vulnerable functions
    if is_vulnerable:
        vulnerable_functions += 1

    # Write the function and its vulnerability status to the result file
    result_file.write(f"Function #{i+1}\nVulnerability: {is_vulnerable}\n\n")

    # Print the result
    print(f"Function #{i+1}\nVulnerability: {is_vulnerable}\n")

    # Sleep for 10 seconds before making the next request
    time.sleep(10)

# Close the result file
result_file.close()

# Print the results metrics
print(f"Total Functions: {total_functions}")
print(f"Vulnerable Functions: {vulnerable_functions}")
print(f"Non-Vulnerable Functions: {total_functions - vulnerable_functions}")
print(f"Vulnerability Rate: {vulnerable_functions / total_functions * 100}%")
print(f"Results saved to file: {result_file_path}")
