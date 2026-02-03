"""
ENHANCED VISUALIZATION CODE
Publication-ready charts for Twitter/LinkedIn
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set style
plt.style.use('dark_background')
sns.set_palette("husl")

# ============================================================================
# HERO VISUAL: Beautiful Cluster Map with Labels
# ============================================================================

def create_hero_cluster_visual(pca_df, output_path="../visuals/hero_cluster_map.png"):
    """
    Create a beautiful, publication-ready cluster visualization
    This is your main visual for social media
    """
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Define colors for each role (consistent across all visuals)
    role_colors = {
        "Attacking Creators": "#FF6B6B",      # Red
        "Defensive Midfielders": "#4ECDC4",   # Teal
        "Centre Backs": "#45B7D1",            # Blue
        "Box-to-Box Midfielders": "#FFA07A",  # Orange
        "Strikers": "#98D8C8"                 # Green
    }
    
    # Plot each cluster
    for role in pca_df['role_name'].unique():
        subset = pca_df[pca_df['role_name'] == role]
        ax.scatter(
            subset['PC1'],
            subset['PC2'],
            c=role_colors.get(role, '#888888'),
            label=role,
            alpha=0.6,
            s=80,
            edgecolors='white',
            linewidths=0.5
        )
    
    # Add role labels (placed at cluster centroids)
    for role in pca_df['role_name'].unique():
        subset = pca_df[pca_df['role_name'] == role]
        centroid_x = subset['PC1'].mean()
        centroid_y = subset['PC2'].mean()
        
        ax.text(
            centroid_x, centroid_y,
            role.upper(),
            fontsize=11,
            fontweight='bold',
            ha='center',
            va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.7, edgecolor='white'),
            color=role_colors.get(role, 'white')
        )
    
    # Annotate some famous players for context
    famous_players = [
        "Mohamed Salah", "Erling Haaland", "Rodri",
        "William Saliba", "Kevin De Bruyne", "Declan Rice"
    ]
    
    texts = []
    for player in famous_players:
        player_data = pca_df[pca_df['player'] == player]
        if not player_data.empty:
            x = player_data['PC1'].values[0]
            y = player_data['PC2'].values[0]
            texts.append(
                ax.text(x, y, player, fontsize=9, alpha=0.9, fontweight='bold')
            )
    
    # Try to adjust text to avoid overlap (optional - requires adjustText package)
    try:
        from adjustText import adjust_text
        adjust_text(texts, arrowprops=dict(arrowstyle='-', color='white', lw=0.5, alpha=0.5))
    except ImportError:
        pass  # Skip if adjustText not installed
    
    # Labels and title
    ax.set_xlabel("PC1 — Vertical Attacking Orientation", fontsize=13, fontweight='bold')
    ax.set_ylabel("PC2 — Involvement & Work Rate", fontsize=13, fontweight='bold')
    ax.set_title(
        "Player Role Profiling via Unsupervised ML\nPremier League 2024/25",
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    
    # Legend
    ax.legend(
        loc='upper left',
        frameon=True,
        fancybox=True,
        shadow=True,
        fontsize=10
    )
    
    # Grid
    ax.grid(alpha=0.2, linestyle='--')
    
    # Branding
    fig.text(
        0.99, 0.01,
        "@MatreAigoukhan | Data: FBref | Method: PCA + K-Means",
        ha='right',
        va='bottom',
        fontsize=9,
        alpha=0.7,
        style='italic'
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
    print(f"✅ Hero visual saved: {output_path}")
    
    return fig


# ============================================================================
# IMPROVED RADAR CHARTS
# ============================================================================

def create_improved_radar(cluster_id, role_name, radar_data, features, 
                          output_path=None, color='#4ECDC4'):
    """
    Enhanced radar chart with better labels and styling
    """
    
    # Better feature names for display
    feature_labels = {
        "touches_def_3rd_pct": "Def Third",
        "touches_mid_3rd_pct": "Mid Third",
        "touches_att_3rd_pct": "Att Third",
        "touches_att_pen_pct": "Penalty Area",
        "tackles": "Tackles",
        "interceptions": "Interceptions",
        "shots": "Shots",
        "xg": "xG"
    }
    
    labels = [feature_labels.get(f, f) for f in features]
    
    # Get values
    values = radar_data.loc[cluster_id, features].values
    values = np.append(values, values[0])
    
    # Calculate angles
    angles = np.linspace(0, 2*np.pi, len(features), endpoint=False)
    angles = np.append(angles, angles[0])
    
    # Create plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    
    # Plot
    ax.plot(angles, values, 'o-', linewidth=2, color=color, label=role_name)
    ax.fill(angles, values, alpha=0.25, color=color)
    
    # Customize
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['25%', '50%', '75%', '100%'], fontsize=9, alpha=0.7)
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Title
    ax.set_title(
        role_name.upper(),
        fontsize=16,
        fontweight='bold',
        pad=20,
        color=color
    )
    
    # Branding
    fig.text(
        0.99, 0.01,
        "@MatreAigoukhan | Data: FBref",
        ha='right',
        va='bottom',
        fontsize=9,
        alpha=0.6
    )
    
    # Save
    if output_path is None:
        output_path = f"../visuals/{role_name.replace(' ', '_').lower()}_radar_enhanced.png"
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
    plt.close()
    
    print(f"✅ Radar saved: {output_path}")

    return fig


# ============================================================================
# RADAR GRID: All Roles at Once
# ============================================================================

def create_radar_grid(radar_data, features, role_labels, 
                      output_path="../visuals/all_roles_radar_grid.png"):
    """
    Create a grid showing all role radars at once
    Perfect for comparison
    """
    
    # Better feature names
    feature_labels = {
        "touches_def_3rd_pct": "Def Third",
        "touches_mid_3rd_pct": "Mid Third",
        "touches_att_3rd_pct": "Att Third",
        "touches_att_pen_pct": "Penalty Area",
        "tackles": "Tackles",
        "interceptions": "Interceptions",
        "shots": "Shots",
        "xg": "xG"
    }
    
    labels = [feature_labels.get(f, f) for f in features]
    
    # Colors for each role
    role_colors = {
        "Attacking Creators": "#FF6B6B",
        "Defensive Midfielders": "#4ECDC4",
        "Centre Backs": "#45B7D1",
        "Box-to-Box Midfielders": "#FFA07A",
        "Strikers": "#98D8C8"
    }
    
    # Create grid (2 rows, 3 columns for 5 roles)
    fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw=dict(projection='polar'))
    axes = axes.flatten()
    
    # Plot each role
    for idx, (cluster_id, role_name) in enumerate(role_labels.items()):
        ax = axes[idx]
        
        # Get values
        values = radar_data.loc[cluster_id, features].values
        values = np.append(values, values[0])
        
        # Angles
        angles = np.linspace(0, 2*np.pi, len(features), endpoint=False)
        angles = np.append(angles, angles[0])
        
        # Plot
        color = role_colors.get(role_name, '#888888')
        ax.plot(angles, values, 'o-', linewidth=2, color=color)
        ax.fill(angles, values, alpha=0.25, color=color)
        
        # Customize
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(['', '', '', ''], fontsize=8)
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.set_title(role_name.upper(), fontsize=12, fontweight='bold', pad=15, color=color)
    
    # Remove extra subplot
    if len(role_labels) < 6:
        fig.delaxes(axes[-1])
    
    # Main title
    fig.suptitle(
        "Player Role Profiles — Behavioral Signatures",
        fontsize=18,
        fontweight='bold',
        y=0.98
    )
    
    # Branding
    fig.text(
        0.99, 0.01,
        "@MatreAigoukhan | Data: FBref | Premier League 2024/25",
        ha='right',
        va='bottom',
        fontsize=10,
        alpha=0.7
    )
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
    print(f"✅ Radar grid saved: {output_path}")
    
    return fig


# ============================================================================
# CLUSTER PROFILE TABLE (as image)
# ============================================================================

def create_cluster_profile_table(cluster_profile, role_labels,
                                  output_path="../visuals/cluster_profile_table.png"):
    """
    Create a clean table showing cluster characteristics
    """
    
    # Select key metrics for display
    display_metrics = [
        'minutes', 'touches', 'touches_att_3rd_pct',
        'shots', 'xg', 'tackles', 'interceptions'
    ]
    
    # Create display dataframe
    display_df = cluster_profile[display_metrics].copy()
    display_df.index = [role_labels[i] for i in display_df.index]
    
    # Round for readability
    display_df = display_df.round(2)
    
    # Rename columns for display
    display_df.columns = ['Mins', 'Touches', 'Att 3rd %', 'Shots', 'xG', 'Tackles', 'Ints']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('tight')
    ax.axis('off')
    
    # Create table
    table = ax.table(
        cellText=display_df.values,
        rowLabels=display_df.index,
        colLabels=display_df.columns,
        cellLoc='center',
        loc='center',
        colWidths=[0.12] * len(display_df.columns)
    )
    
    # Style
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)
    
    # Color header
    for i in range(len(display_df.columns)):
        table[(0, i)].set_facecolor('#2C3E50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # Color row labels
    for i in range(1, len(display_df) + 1):
        table[(i, -1)].set_facecolor('#34495E')
        table[(i, -1)].set_text_props(weight='bold', color='white')
    
    # Title
    plt.title(
        "Cluster Profiles — Average Stats per Role",
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    
    # Branding
    fig.text(
        0.99, 0.01,
        "@MatreAigoukhan | Data: FBref",
        ha='right',
        va='bottom',
        fontsize=9,
        alpha=0.7
    )
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Table saved: {output_path}")