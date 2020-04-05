#include "Lepton_I2C.h"

#include "leptonSDKEmb32PUB/LEPTON_SDK.h"
#include "leptonSDKEmb32PUB/LEPTON_SYS.h"
#include "leptonSDKEmb32PUB/LEPTON_OEM.h"
#include "leptonSDKEmb32PUB/LEPTON_Types.h"
#include "leptonSDKEmb32PUB/LEPTON_AGC.h"

bool _connected;

LEP_CAMERA_PORT_DESC_T _port;

int lepton_connect() {
	LEP_OpenPort(1, LEP_CCI_TWI, 400, &_port);
	_connected = true;
	return 0;
}

void lepton_perform_ffc() {
	if(!_connected) {
		lepton_connect();
	}
	LEP_RunSysFFCNormalization(&_port);
}

//presumably more commands could go here if desired

void lepton_reboot() {
	if(!_connected) {
		lepton_connect();
	}
	LEP_RunOemReboot(&_port);
}

void lepton_agcDisable()
{
if (!_connected){
        lepton_connect();
    }
    LEP_SetAgcEnableState(&_port, LEP_AGC_ENABLE);
}


void lepton_gainmode_low()
{
if (!_connected){
        lepton_connect();
    }
LEP_SetAgcHeqClipLimitLow(&_port,LEP_AGC_HEQ_CLIP_LIMIT_LOW);
}
