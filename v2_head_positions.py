import os
import pandas as pd
import matplotlib.pyplot as plt

def create_combined_chart(before_files, after_files, folder_path, yes_list, session_name):
    # Construct the full yes_list with session_name prefix
    full_yes_list = [f'{session_name}_{i}' for i in yes_list]

    yes_files = [f for f in before_files if any(yes in f for yes in full_yes_list)]
    no_files = [f for f in before_files if f not in yes_files]
    
    num_yes_files = len(yes_files)
    num_no_files = len(no_files)
    max_files = max(num_yes_files, num_no_files)
    
    fig, axes = plt.subplots(max_files, 4, figsize=(24, max_files * 4))
    
    # Add headers at the top
    fig.text(0.25, 0.95, 'Good Signal', ha='center', va='center', fontsize=20, weight='bold')
    fig.text(0.75, 0.95, 'Bad Signal', ha='center', va='center', fontsize=20, weight='bold')

    axes[0, 0].set_title('Before', fontsize=14)
    axes[0, 1].set_title('After', fontsize=14)
    axes[0, 2].set_title('Before', fontsize=14)
    axes[0, 3].set_title('After', fontsize=14)

    for i in range(max_files):
        if i < num_yes_files:
            before_file_yes = yes_files[i]
            after_file_yes = before_file_yes.replace('_before', '_after')
            before_data_yes = pd.read_csv(os.path.join(folder_path, before_file_yes))
            after_data_yes = pd.read_csv(os.path.join(folder_path, after_file_yes))
            
            combined_before_yes = pd.concat([
                before_data_yes[' pose_Rx'].rename('pose_Rx'),
                before_data_yes[' pose_Ry'].rename('pose_Ry'),
                before_data_yes[' pose_Rz'].rename('pose_Rz')
            ], axis=1)

            combined_after_yes = pd.concat([
                after_data_yes[' pose_Rx'].rename('pose_Rx'),
                after_data_yes[' pose_Ry'].rename('pose_Ry'),
                after_data_yes[' pose_Rz'].rename('pose_Rz')
            ], axis=1)

            combined_before_yes.plot(ax=axes[i, 0], color=['blue', 'orange', 'green'])
            combined_after_yes.plot(ax=axes[i, 1], color=['blue', 'orange', 'green'])

            csv_name_before_yes = os.path.splitext(before_file_yes)[0]
            csv_name_after_yes = os.path.splitext(after_file_yes)[0]

            axes[i, 0].set_title(csv_name_before_yes)
            axes[i, 1].set_title(csv_name_after_yes)
            axes[i, 0].set_xlabel('Index')
            axes[i, 1].set_xlabel('Index')
            axes[i, 0].set_ylabel('Values')
            axes[i, 1].set_ylabel('Values')
        
        if i < num_no_files:
            before_file_no = no_files[i]
            after_file_no = before_file_no.replace('_before', '_after')
            before_data_no = pd.read_csv(os.path.join(folder_path, before_file_no))
            after_data_no = pd.read_csv(os.path.join(folder_path, after_file_no))
            
            combined_before_no = pd.concat([
                before_data_no[' pose_Rx'].rename('pose_Rx'),
                before_data_no[' pose_Ry'].rename('pose_Ry'),
                before_data_no[' pose_Rz'].rename('pose_Rz')
            ], axis=1)

            combined_after_no = pd.concat([
                after_data_no[' pose_Rx'].rename('pose_Rx'),
                after_data_no[' pose_Ry'].rename('pose_Ry'),
                after_data_no[' pose_Rz'].rename('pose_Rz')
            ], axis=1)

            combined_before_no.plot(ax=axes[i, 2], color=['blue', 'orange', 'green'])
            combined_after_no.plot(ax=axes[i, 3], color=['blue', 'orange', 'green'])

            csv_name_before_no = os.path.splitext(before_file_no)[0]
            csv_name_after_no = os.path.splitext(after_file_no)[0]

            axes[i, 2].set_title(csv_name_before_no)
            axes[i, 3].set_title(csv_name_after_no)
            axes[i, 2].set_xlabel('Index')
            axes[i, 3].set_xlabel('Index')
            axes[i, 2].set_ylabel('Values')
            axes[i, 3].set_ylabel('Values')

    # Adjust legends to show only 'pose_Rx', 'pose_Ry', and 'pose_Rz'
    handles, labels = axes[0, 0].get_legend_handles_labels()
    new_labels = ['pose_Rx', 'pose_Ry', 'pose_Rz']
    
    for ax in axes.flatten():
        ax.legend(handles, new_labels, loc='best')
    
    plt.tight_layout(rect=[0, 0, 1, 0.93])

    # Construct the correct output path including the full directory structure
    output_filename = os.path.join(folder_path, f'{session_name}_pose.png')
    plt.savefig(output_filename)
    plt.close()

def process_csv_files(base_folder, session_name, yes_list):
    folder_path = os.path.join(base_folder, session_name)
    
    before_files = sorted([f for f in os.listdir(folder_path) if f.endswith('_before.csv')])
    after_files = sorted([f for f in os.listdir(folder_path) if f.endswith('_after.csv')])
    
    create_combined_chart(before_files, after_files, folder_path, yes_list, session_name)

# Replace with the actual session name and yes_list array
base_folder = '/Users/jiya/openface_results/D124'
session_name = 'D124_S4'
yes_list = ['8', '10'] 
#yes_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # Only input the indices here
process_csv_files(base_folder, session_name, yes_list)