import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def check_cluster_distribution(pca_df):
    """Check if clusters are balanced or if one cluster dominates"""
    
    print("="*60)
    print("CLUSTER SIZE DISTRIBUTION")
    print("="*60)
    
    sizes = pca_df['role_name'].value_counts().sort_index()
    print("\nPlayers per role:")
    print(sizes)
    
    print(f"\nTotal players: {len(pca_df)}")
    print(f"\nPercentage distribution:")
    for role, count in sizes.items():
        pct = (count / len(pca_df)) * 100
        print(f"{role}: {pct:.1f}%")
    
    # Visual
    plt.figure(figsize=(10, 6))
    sizes.plot(kind='bar', color='steelblue')
    plt.title("Players per Role", fontsize=14, fontweight='bold')
    plt.xlabel("Role")
    plt.ylabel("Number of Players")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("../visuals/cluster_distribution.png", dpi=300, bbox_inches='tight')
    print("\n✅ Chart saved: cluster_distribution.png")

def check_top_players_per_cluster(pca_df, df, top_n=15):
    """List top players by minutes in each cluster - sanity check"""
    
    print("\n" + "="*60)
    print("TOP PLAYERS PER ROLE (By Minutes)")
    print("="*60)
    
    # Merge to get minutes
    merged = pca_df.merge(df[['player', 'minutes']], on='player', how='left')
    
    for role in sorted(pca_df['role_name'].unique()):
        role_df = merged[merged['role_name'] == role]
        top_players = role_df.nlargest(top_n, 'minutes')
        
        print(f"\n{role.upper()}:")
        print("-" * 40)
        for idx, row in enumerate(top_players.itertuples(), 1):
            print(f"{idx:2d}. {row.player:<30} ({row.minutes:>4.0f} mins)")
        
        # Quick sanity check
        print(f"\n👉 Do these {top_n} players belong together?")

def check_position_alignment(pca_df):
    """Check how well cluster roles align with official positions"""
    
    print("\n" + "="*60)
    print("POSITION vs ROLE ALIGNMENT")
    print("="*60)
    
    # Confusion matrix
    confusion = pd.crosstab(
        pca_df['position'],
        pca_df['role_name'],
        margins=True
    )
    
    print("\nConfusion Matrix:")
    print(confusion)
    
    # Calculate alignment percentage
    # (This is simplified - assumes 1:1 mapping)
    # For more complex analysis, use silhouette score
    
    print("\n" + "="*60)
    print("INTERPRETATION GUIDE:")
    print("="*60)
    print("""
    ✅ GOOD: Positions cluster together (e.g., all CBs in Centre Backs role)
    ⚠️  INTERESTING: Mixed positions in one role (e.g., role is behavior-based)
    ❌ BAD: Random distribution (clustering failed)
    
    Example good pattern:
    - "Centre Backs" role = mostly DF players
    - "Strikers" role = mostly FW players
    - "Box-to-Box" role = mix of MF/DF (expected!)
    """)

def validate_known_players(pca_df):
    """Check if well-known players are in expected roles"""
    
    print("\n" + "="*60)
    print("KNOWN PLAYERS VALIDATION")
    print("="*60)
    
    # Define expectations
    expected_roles = {
        "Mohamed Salah": "Attacking Creators or Strikers",
        "Erling Haaland": "Strikers",
        "Rodri": "Defensive Midfielders",
        "William Saliba": "Centre Backs",
        "Kevin De Bruyne": "Attacking Creators or Box-to-Box",
        "Declan Rice": "Box-to-Box Midfielders or Defensive Midfielders",
        "Bukayo Saka": "Attacking Creators",
    }
    
    print("\nValidation results:")
    print("-" * 60)
    
    for player, expected in expected_roles.items():
        actual = pca_df[pca_df['player'] == player]['role_name'].values
        
        if len(actual) > 0:
            actual_role = actual[0]
            match = "✅" if any(e in actual_role for e in expected.split(" or ")) else "⚠️"
            print(f"{match} {player:<25} → {actual_role:<30} (Expected: {expected})")
        else:
            print(f"❓ {player:<25} → NOT FOUND (may not have 500+ mins)")


def check_cluster_separation(pca_df):
    """Visual check of cluster separation in PCA space"""
    
    print("\n" + "="*60)
    print("CLUSTER SEPARATION QUALITY")
    print("="*60)
    
    plt.figure(figsize=(12, 8))
    
    # Plot each cluster with different color
    for role in pca_df['role_name'].unique():
        subset = pca_df[pca_df['role_name'] == role]
        plt.scatter(
            subset['PC1'],
            subset['PC2'],
            label=role,
            alpha=0.6,
            s=50
        )
    
    plt.xlabel("PC1 - Vertical Attacking Orientation", fontsize=12)
    plt.ylabel("PC2 - Involvement & Work Rate", fontsize=12)
    plt.title("Cluster Separation in PCA Space", fontsize=14, fontweight='bold')
    plt.legend(loc='best')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("../visuals/cluster_separation.png", dpi=300, bbox_inches='tight')
    
    print("\n✅ Chart saved: cluster_separation.png")
    print("""
    INTERPRETATION:
    ✅ GOOD: Clear separation between clusters (distinct groups)
    ⚠️  OK: Some overlap (expected for similar roles)
    ❌ BAD: Complete overlap (clustering failed)
    """)

def find_edge_cases(pca_df):
    """Find players on cluster boundaries - interesting cases"""
    
    print("\n" + "="*60)
    print("EDGE CASES & INTERESTING PLAYERS")
    print("="*60)
    
    # For each role, find players closest to other clusters
    # This identifies "hybrid" players
    
    from sklearn.metrics.pairwise import euclidean_distances
    
    # Calculate distance of each player to all cluster centers
    # (This requires the KMeans model which we don't have here)
    # Simplified version: find players at extreme PCA values
    
    print("\nPlayers at PCA extremes (potential outliers/unique profiles):")
    print("-" * 60)
    
    # Highest PC1 (most attacking)
    top_pc1 = pca_df.nlargest(5, 'PC1')
    print("\nMost Attacking Orientation (High PC1):")
    for _, row in top_pc1.iterrows():
        print(f"  {row['player']:<30} PC1={row['PC1']:.2f}, Role={row['role_name']}")
    
    # Lowest PC1 (most defensive)
    bottom_pc1 = pca_df.nsmallest(5, 'PC1')
    print("\nMost Defensive Orientation (Low PC1):")
    for _, row in bottom_pc1.iterrows():
        print(f"  {row['player']:<30} PC1={row['PC1']:.2f}, Role={row['role_name']}")
    
    # Highest PC2 (highest involvement)
    top_pc2 = pca_df.nlargest(5, 'PC2')
    print("\nHighest Involvement (High PC2):")
    for _, row in top_pc2.iterrows():
        print(f"  {row['player']:<30} PC2={row['PC2']:.2f}, Role={row['role_name']}")
    
    # Lowest PC2 (lowest involvement)
    bottom_pc2 = pca_df.nsmallest(5, 'PC2')
    print("\nLowest Involvement (Low PC2):")
    for _, row in bottom_pc2.iterrows():
        print(f"  {row['player']:<30} PC2={row['PC2']:.2f}, Role={row['role_name']}")
