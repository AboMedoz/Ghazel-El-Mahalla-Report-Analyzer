import matplotlib.pyplot as plt
import seaborn as sns


class PlotDataFrame:
    def __init__(self, df, file_name):
        self.df = df
        self.file_name = file_name

        failed_machines = self.df.loc[self.df['State'] == 'Failure', self.df.columns[0]].astype(str).tolist()
        offline_machines = self.df.loc[self.df['State'] == 'Offline', self.df.columns[0]].astype(str).tolist()
        run_machines = self.df.loc[self.df['State'] == 'Run', self.df.columns[0]].astype(str).tolist()
        service_machines = self.df.loc[self.df['State'] == 'Service', self.df.columns[0]].astype(str).tolist()
        stop_machines = self.df.loc[self.df['State'] == 'Stop', self.df.columns[0]].astype(str).tolist()

        self.status_text = (
            f"Failed Machines: {len(failed_machines)} "
            f"\nOffline Machines: {len(offline_machines)}"
            f"\nRun Machines: {len(run_machines)}"
            f"\nService Machines: {len(service_machines)}"
            f"\nStop Machines: {len(stop_machines)}"
        )

    def plot_label(self, label):
        label_index = {
            'Production': 3,
            'Efficiency': 4,
            'Availability': 5
        }.get(label, None)

        # yarn_map = machine -> yarncount
        yarn_map = self.df.set_index(self.df.iloc[:, 0])[self.df.columns[1]].to_dict()

        plt.figure(figsize=(20, 30))
        ax = sns.barplot(
            data=self.df[self.df.iloc[:, 0] != 'Total'],
            x=self.df.iloc[:, label_index],
            y=self.df.iloc[:, 0],
            hue="State", dodge=False, palette="Set2"
        )
        # mean & median
        mean_val = self.df.iloc[:, label_index].mean()
        median_val = self.df.iloc[:, label_index].median()
        plt.axvline(mean_val, color="red", linestyle="--", linewidth=2, label=f"Mean = {mean_val:.1f}")
        plt.axvline(median_val, color="green", linestyle="-.", linewidth=2, label=f"Median = {median_val:.1f}")
        # status box
        plt.text(
            x=0.95, y=0.95,
            s=self.status_text,
            transform=plt.gca().transAxes,
            ha='right', va='top', fontsize=20,
            bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white', alpha=0.7)
        )
        # production note
        if label == 'Production':
            prod_val = self.df.loc[self.df.iloc[:, 0] == 'Total', self.df.iloc[:, 3]].iloc[0]
            plt.text(
                x=0.95, y=0.5,
                s=f"Actual Production: {prod_val}Kg\nTarget: 9000Kg",
                transform=plt.gca().transAxes,
                ha='right', va='top', fontsize=15,
                bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white', alpha=0.7)
            )
        # annotate yarn values
        labels = [lab.get_text() for lab in ax.get_yticklabels()]
        max_width_by_machine = {}
        y_center_by_machine = {}
        for patch in ax.patches:
            y_center = patch.get_y() + patch.get_height() / 2.0
            idx = int(round(y_center))
            if 0 <= idx < len(labels):
                mach = labels[idx]
                w = patch.get_width()
                if (mach not in max_width_by_machine) or (w > max_width_by_machine[mach]):
                    max_width_by_machine[mach] = w
                    y_center_by_machine[mach] = y_center

        xmax = ax.get_xlim()[1]
        offset = 0.01 * (xmax if xmax != 0 else 1)
        for mach, w in max_width_by_machine.items():
            if mach in yarn_map:
                val = yarn_map[mach]
                ax.text(
                    w + offset, y_center_by_machine[mach],
                    f"Yarn: {val}",
                    va='center', ha='left', fontsize=9, color='black'
                )
        plt.title(f"Machine {label} in {self.file_name}", fontsize=16)
        plt.xlabel(label, fontsize=14)
        plt.ylabel("Machine No", fontsize=14)
        plt.legend(title="State")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        return plt.gcf()
