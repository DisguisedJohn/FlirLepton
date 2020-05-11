#include <iostream>
#include "Lepton_I2C.h"

using namespace std;

int main()
{
    cout << "Starting inital setup. << endl;

    lepton_agcDisable();    //Disabling auto gain control
    lepton_perform_ffc();   //Detector calibration

    cout << "Inital setup done. << endl;

    return 0;
}
