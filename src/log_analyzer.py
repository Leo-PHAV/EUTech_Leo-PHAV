import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import re
from datetime import datetime

class SystemLogAnalyzer:
    def __init__(self, log_path, output_dir='reports'):
        self.log_path = log_path
        self.output_dir = output_dir
        self.df = None
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def parse_logs(self):
        log_data = []
        pattern = re.compile(r'(\w{3}\s+\d+\s\d+:\d+:\d+)\s+(\S+)\s+(\S+)?\[?\d*\]?:\s+(.*)')
        
        try:
            with open(self.log_path, 'r', encoding='latin-1') as file:
                for line in file:
                    match = pattern.search(line)
                    if match:
                        timestamp_str = f"{datetime.now().year} {match.group(1)}"
                        log_data.append({
                            'timestamp': pd.to_datetime(timestamp_str, format='%Y %b %d %H:%M:%S'),
                            'hostname': match.group(2),
                            'service': match.group(3),
                            'message': match.group(4),
                            'level': 'ERROR' if any(x in line.lower() for x in ['error', 'fail', 'critical', 'fatal']) else 'INFO'
                        })
            self.df = pd.DataFrame(log_data)
        except FileNotFoundError:
            print(f"Error: {self.log_path} not found.")
            return

    def generate_visualizations(self):
        if self.df is None or self.df.empty:
            return

        sns.set_style("darkgrid")

        plt.figure(figsize=(10, 6))
        level_counts = self.df['level'].value_counts()
        plt.pie(level_counts, labels=level_counts.index, autopct='%1.1f%%', colors=['#66b3ff','#ff9999'])
        plt.title('Distribution of Log Levels')
        plt.savefig(os.path.join(self.output_dir, 'log_distribution_pie.png'))
        plt.close()

        plt.figure(figsize=(12, 6))
        self.df['hour'] = self.df['timestamp'].dt.hour
        hourly_logs = self.df.groupby(['hour', 'level']).size().unstack(fill_value=0)
        hourly_logs.plot(kind='bar', stacked=True, color=['#ff9999', '#66b3ff'])
        plt.title('Log Frequency by Hour')
        plt.xlabel('Hour of Day')
        plt.ylabel('Count')
        plt.legend(title='Level')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'hourly_analysis_bar.png'))
        plt.close()

    def export_results(self):
        if self.df is not None:
            html_path = os.path.join(self.output_dir, 'analysis_report.html')
            self.df.to_html(html_path)
            
            summary_path = os.path.join(self.output_dir, 'summary.txt')
            with open(summary_path, 'w') as f:
                f.write(f"Log Analysis Summary - {datetime.now()}\n")
                f.write(f"Total entries: {len(self.df)}\n")
                f.write(f"Errors found: {len(self.df[self.df['level'] == 'ERROR'])}\n")

if __name__ == "__main__":
    # Liste des fichiers logs pertinents identifiés (Conformément à la consigne)
    log_files = [
        '/var/log/syslog',   # Messages système généraux
        '/var/log/auth.log', # Tentatives de connexion (User login times)
        '/var/log/kern.log'  # Messages du noyau (Hardware/Resources)
    ]
    
    # On initialise l'analyseur sur le premier fichier existant pour créer l'objet
    analyzer = SystemLogAnalyzer(log_files[0])
    
    # Liste pour accumuler tous les DataFrames
    all_dfs = []
    
    for path in log_files:
        if os.path.exists(path):
            analyzer.log_path = path
            analyzer.parse_logs()
            if analyzer.df is not None:
                all_dfs.append(analyzer.df)
                print(f"Successfully parsed: {path}")
    
    # Fusion de toutes les données pour une analyse globale
    if all_dfs:
        analyzer.df = pd.concat(all_dfs, ignore_index=True)
        analyzer.generate_visualizations()
        analyzer.export_results()
        print("Global analysis complete for all identified log files.")