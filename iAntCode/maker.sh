cd build
rm -r * 
cmake ..
make 
cd ..
argos3 -c experiments/iAnt_linux.argos
