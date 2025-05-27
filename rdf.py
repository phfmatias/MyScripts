import matplotlib.pyplot as plt  
import matplotlib.image as mpimg 
import matplotlib.patches as patches  
import numpy as np  

c2 = np.loadtxt("c2_nc.xvg", comments=["#", "@"])  
c4 = np.loadtxt("c4_nc.xvg", comments=["#", "@"])
c5 = np.loadtxt("c5_nc.xvg", comments=["#", "@"])
c9 = np.loadtxt("c9_nc.xvg", comments=["#", "@"])
# c10 = np.loadtxt("c10_nc.xvg", comments=["#", "@"])
c13 = np.loadtxt("c13_nc.xvg", comments=["#", "@"])


#print nm when gr is max and the gr

c9_max_nm = c9[np.argmax(c9[:,1]), 0]
c9_max_gr = np.max(c9[:,1])

c2_max_nm = c2[np.argmax(c2[:,1]), 0]
c2_max_gr = np.max(c2[:,1])

c4_max_gr = np.max(c4[:,1])
c5_max_gr = np.max(c5[:,1])
c13_max_gr = np.max(c13[:,1])

print(f"c9_max_nm: {c9_max_nm:.2f} nm, c9_max_gr: {c9_max_gr:.2f}")
print(f"c2_max_nm: {c2_max_nm:.2f} nm, c2_max_gr: {c2_max_gr:.2f}")


#printing order of the peaks like C9 > C2 ....

print(f"c9_max_gr: {c9_max_gr:.2f} > c2_max_gr: {c2_max_gr:.2f} > c4_max_gr: {c4_max_gr:.2f} > c5_max_gr: {c5_max_gr:.2f} > c13_max_gr: {c13_max_gr:.2f}")

fig = plt.figure(figsize=(8, 5))
ax = fig.add_subplot(111)
ax.plot(c2[:,0]*10, c2[:,1], label="C2 $\cdots$ N", color="#7b0204")
ax.plot(c4[:,0]*10, c4[:,1], label="C4 $\cdots$ N", color="#018e00")
ax.plot(c5[:,0]*10, c5[:,1], label="C5 $\cdots$ N", color="#025193")
ax.plot(c9[:,0]*10, c9[:,1], label="C9 $\cdots$ N", color="#ffa514")
# ax.plot(c10[:,0]*10, c10[:,1], label="C10 $\cdots$ N", color="#b300b3")
ax.plot(c13[:,0]*10, c13[:,1], label="C13 $\cdots$ N", color="#000000")

ax.set_ylim(0,5.5)

plt.xlabel("r (Å)")
plt.ylabel("g(r)")
ax.axhline(y=1, color="gray", linestyle="--", linewidth=0.8)
ax.legend()
ax.grid(True, linestyle="dotted", alpha=0.5)


img = mpimg.imread("label.png")
image_ax = fig.add_axes([0.55, 0.55, 0.2, 0.45])  # [left, bottom, width, height] in figure coordinates
image_ax.imshow(img)
image_ax.axis("off")  # Hide axes around the image


plt.savefig("rdf.png", dpi=300, bbox_inches="tight")