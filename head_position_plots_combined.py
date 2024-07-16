import os
import pandas as pd
import matplotlib.pyplot as plt

def create_combined_chart(before_files, after_files, folder_path):
    num_files = len(before_files)
    fig, axes = plt.subplots(num_files, 2, figsize=(12, num_files * 4))

    for i, (before_file, after_file) in enumerate(zip(before_files, after_files)):
        before_data = pd.read_csv(os.path.join(folder_path, before_file))
        after_data = pd.read_csv(os.path.join(folder_path, after_file))

        combined_before = pd.concat([
            before_data[' pose_Rx'].rename('pose_Rx_before'),
            before_data[' pose_Ry'].rename('pose_Ry_before'),
            before_data[' pose_Rz'].rename('pose_Rz_before')
        ], axis=1)

        combined_after = pd.concat([
            after_data[' pose_Rx'].rename('pose_Rx_after'),
            after_data[' pose_Ry'].rename('pose_Ry_after'),
            after_data[' pose_Rz'].rename('pose_Rz_after')
        ], axis=1)

        combined_before.plot(kind='bar', ax=axes[i, 0], color=['blue', 'orange', 'green'])
        combined_after.plot(kind='bar', ax=axes[i, 1], color=['blue', 'orange', 'green'])

        csv_name_before = os.path.splitext(before_file)[0]
        csv_name_after = os.path.splitext(after_file)[0]

        axes[i, 0].set_title(f'Combined Before - {csv_name_before}')
        axes[i, 1].set_title(f'Combined After - {csv_name_after}')
        axes[i, 0].set_xlabel('Index')
        axes[i, 1].set_xlabel('Index')
        axes[i, 0].set_ylabel('Values')
        axes[i, 1].set_ylabel('Values')

    plt.tight_layout()
    output_filename = 'combined_pose_values.png'
    plt.savefig(output_filename)
    plt.close()

def process_csv_files(folder_path):
    before_files = sorted([f for f in os.listdir(folder_path) if f.endswith('_before.csv')])
    after_files = sorted([f for f in os.listdir(folder_path) if f.endswith('_after.csv')])

    create_combined_chart(before_files, after_files, folder_path)

#Replace with path of folder that contains CSV files 
folder_path = 'D103/D103_S1'
process_csv_files(folder_path)


