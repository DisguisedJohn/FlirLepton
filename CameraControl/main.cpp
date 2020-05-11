#include <iostream>
#include "Lepton_I2C.h"

using namespace std;

int main()
{
    cout << "Hello world!" << endl;

    //lepton_reboot();
    lepton_agcDisable();
    //lepton_perform_ffc();
    //lepton_gainmode_low();
    return 0;
}
