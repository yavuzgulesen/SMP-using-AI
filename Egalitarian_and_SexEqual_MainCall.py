# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 02:22:51 2020

@author: YavuzGulesen
"""
from Egalitarian_and_SexEqual import Egalitarian_SexEqual
from GentProsser import GentProsser
import matplotlib.pyplot as plt


n1 = 25
n2 = n1
p1 = 0.2
p2 = 0.2
step = 5000
mpref, wpref = GentProsser(n1, n2, p1, p2)



f_eg, cost_eg, nbp_eg, ns_eg, fs_eg, costs_eg, total_steps = Egalitarian_SexEqual(mpref, wpref, step, "eg")
f_se, cost_se, nbp_se, ns_se, fs_se, costs_se, total_steps_se = Egalitarian_SexEqual(mpref, wpref, step, "se")



fig, axs = plt.subplots(2)

axs[0].plot(fs_eg, "tab:blue")
axs[0].plot(costs_eg, "tab:pink")
axs[0].set_title("Egalitarian SMTI, blue: f(nbp+ns), pink: cost")
axs[0].set_xlabel("step")

axs[1].plot(fs_se, "tab:blue")
axs[1].plot(costs_se, "tab:pink")
axs[1].set_title("Sex-Equal SMTI, blue: f(nbp+ns), pink: cost")
axs[1].set_xlabel("# steps")
fig.tight_layout()

plt.show()

#fig, axs = plt.subplots(2)

print("--------------")
print("| Egalitarian results")
print("| f:", f_eg)
print("| cost:", cost_eg)
print("| nbp:", nbp_eg)
print("| ns:", ns_eg)
print("| step:", total_steps)
print("--------------")

print("| SexEqual results")
print("| f:", f_se)
print("| cost:", cost_se)
print("| nbp:", nbp_se)
print("| ns:", ns_se)
print("| step:", total_steps_se)
print("--------------")

