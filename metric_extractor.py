import lizard
import csv
import os

def extract_metrics(project_path, output_csv):
    features = []

    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(('.py', '.java', '.html', '.css')):
                file_path = os.path.join(root, file)
                analysis = lizard.analyze_file(file_path)

                total_loc = analysis.nloc
                lloc = sum(f.length for f in analysis.function_list)  # FIXED LINE
                total_functions = len(analysis.function_list)
                num_loops = sum(f.cyclomatic_complexity for f in analysis.function_list)
                imports = sum(1 for line in open(file_path, encoding='utf-8', errors='ignore') if 'import' in line)

                features.append([
                    total_loc, lloc, 0,  # dummy for TNA
                    total_functions, 0,  # dummy for PUA
                    lloc, 0,  # TLLOC, NLE
                    num_loops, total_loc,  # TNLPM, TLOC
                    num_loops // (total_functions or 1),  # NLPM
                    total_functions, total_functions,  # NLM, TNLM
                    imports, lloc,  # NOI, TNOS
                    lloc // (total_functions or 1),  # NOS
                    num_loops  # NL
                ])

    # Save to CSV
    with open(output_csv, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "TCLOC", "LLOC", "TNA", "NM", "PUA", "TLLOC", "NLE", "TNLPM",
            "TLOC", "NLPM", "NLM", "TNLM", "NOI", "TNOS", "NOS", "NL"
        ])
        writer.writerows(features)

# DO NOT call extract_metrics() here!
