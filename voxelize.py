#Voxelize .xyz data
#Mathew Cherukara, APS, Argonne
import os
import sys
import numpy as np


if (len(sys.argv)<6): 
    print "ERROR:Usage is input_file output_file bin sizes"
    exit()

fname=sys.argv[1]
oname=sys.argv[2]
ifile = open(fname, 'r')
nats=int(ifile.readline())
hdr=ifile.readline() #Header line
data=np.zeros((nats,3),float)

ax=int(sys.argv[3])
ay=int(sys.argv[4])
az=int(sys.argv[5])

i=0
for line in ifile:
  tmp=line.split() 
  if(tmp[0]=='Co'): #Modify when you have more elements
   data[i,0],data[i,1],data[i,2]=float(tmp[1]),float(tmp[2]),float(tmp[3])
   i+=1

natsel=i
print "Number of selected atoms", natsel

xmin,xmax=min(data[:,0]),max(data[:,0])
ymin,ymax=min(data[:,1]),max(data[:,1])
zmin,zmax=min(data[:,2]),max(data[:,2])
print "Original atom ranges", xmin, xmax, ymin, ymax, zmin, zmax
if(xmin<0):data[:,0]-=xmin
if(ymin<0):data[:,1]-=ymin
if(zmin<0):data[:,2]-=zmin
xmin,xmax=min(data[:,0]),max(data[:,0])
ymin,ymax=min(data[:,1]),max(data[:,1])
zmin,zmax=min(data[:,2]),max(data[:,2])
print "Shifted atom ranges", xmin, xmax, ymin, ymax, zmin, zmax

nx=int((xmax - xmin)/ax) + 1
ny=int((ymax - ymin)/ay) + 1
nz=int((zmax - zmin)/az) + 1

print "nx,ny,nz", nx,ny,nz
dens=np.zeros((nx,ny,nz),float)

for i in range (natsel):
  b1=int((data[i,0]-xmin)/ax)
  b2=int((data[i,1]-ymin)/ay)
  b3=int((data[i,2]-zmin)/az)
  dens[b1,b2,b3]+=1
nmax=np.max(dens)
print "Max no of atoms", nmax
dens/=nmax #Normalize to max no of atoms

#Write data to XYZ
ofile=open(oname+'.xyz','w')
ofile.write("%d\n" %(nx*ny*nz))
ofile.write("Type X Y Z\n")
for i in range(0,nx):
 for j in range(0,ny):
  for k in range(0,nz):
   ofile.write("%.2f %.2f %.2f %.4f\n" %(i*ax,j*ax,k*ax,dens[i,j,k]))
ofile.close()

