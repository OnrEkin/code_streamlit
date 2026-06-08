import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Sayfa Ayarları
st.set_page_config(page_title="Kelly Criterion Simulation", layout="centered")
st.title("Kelly Criterion Growth Simulation")

# Sabit Seed ve Master Rolls (Orijinal koddaki gibi sabit bırakıldı)
np.random.seed(42)
max_steps = 1000
master_dice_rolls = np.random.rand(max_steps)

# SIMULATION FONKSİYONU
def calculate_bankroll_path(f, p, current_steps):
    bankroll = 1000.0
    history = [bankroll]
    
    if f <= 0:
        return [1000.0] * (current_steps + 1)
    
    for i in range(current_steps):
        if bankroll <= 1:
            history.append(1)
            continue
            
        dice_roll = master_dice_rolls[i]
        bet_amount = bankroll * f
        
        if dice_roll < p:
            bankroll = bankroll + bet_amount 
        else:
            bankroll = bankroll - bet_amount 
            
        if bankroll < 1:
            bankroll = 1
            
        history.append(bankroll)
        
    return history

# STREAMLIT SLIDER KONTROLLERİ
st.markdown("### Choose Your Parameters")
current_steps = st.slider('Hands Played (Steps)', min_value=1, max_value=max_steps, value=150, step=1)
p = st.slider('Win Chance (p)', min_value=0.00, max_value=1.00, value=0.60, step=0.01)
f_percent = st.slider('Risk % (f)', min_value=0.0, max_value=100.0, value=15.0, step=0.5)

# MATEMATİKSEL HESAPLAMALAR
f_actual = f_percent / 100.0  
opt_f = max(0, p - (1 - p))

new_path_opt = calculate_bankroll_path(opt_f, p, current_steps)
new_path_user = calculate_bankroll_path(f_actual, p, current_steps)

# DİNAMİK BİLGİLENDİRME MESAJLARI VE RENKLER
if opt_f <= 0:
    user_color = 'gray'
    st.error('You have no chance of winning in the long run. Do not play.')
elif abs(f_actual - opt_f) < 0.02:
    user_color = 'lime'
    st.success('Great! You are on the optimum growth path.')
elif f_actual >= opt_f * 2:
    user_color = 'crimson'
    st.error('You took too much risk! You will eventually lose everything.')
elif f_actual > opt_f:
    user_color = 'darkorange'
    st.warning('Unnecessary risk. You are betting more than the optimum.')
else:
    user_color = 'royalblue'
    st.info('You are playing safely, but this is not the fastest growth.')

# GRAFİK ÇİZİM ALANI
fig, ax = plt.subplots(figsize=(12, 6))

x_data = range(current_steps + 1)

# Çizgiler
ax.plot(x_data, new_path_opt, label='Goal: Optimum Growth (Kelly)', color='forestgreen', linewidth=4, alpha=0.4)
ax.plot(x_data, new_path_user, label='Your Choice', color=user_color, linewidth=2.5)

# Dekorasyonlar
ax.set_yscale('log')
ax.set_xlabel('Hands Played', fontsize=12)
ax.set_ylabel('Bankroll Size "Logarithmic"', fontsize=12)
# Orijinal koddaki küçük yazım hatası düzeltildi (100 -> 1000)
ax.axhline(1000, color='gray', linestyle='--', label='Start with 1000')
ax.grid(True, which="both", ls="-", alpha=0.2)
ax.legend(loc='upper left', fontsize=11)

# Ekran Limitleri
ax.set_xlim(0, current_steps)
max_val = max(max(new_path_opt), max(new_path_user))
ax.set_ylim(0.8, max(1000, max_val * 5))

# Grafiği Ekrana Bas
st.pyplot(fig)
