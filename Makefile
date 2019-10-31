# Port can be defined globally but defaults to ttyUSB0
PORT ?= ttyUSB0

.PHONY: shell install_common install_multicast

shell:
	mpfshell -o ${PORT}


install_multicast: install_common
	mpfshell -o ${PORT} -n -c "put scripts/weather/with_multicast.py multi.py"
	# modify pin number ifneedbe
	echo -e "from multi import main\n\nmain(4)" > .tmp/mult-main.py
	mpfshell -o ${PORT} -n -c "put .tmp/mult-main.py main.py"


install_common:
	mpfshell -o ${PORT} -n -c "put scripts/weather/wifi.py wifi.py"
	mpfshell -o ${PORT} -n -c "put scripts/weather/sleep.py sleep.py"

flash:
	@echo "Run this:"
	@echo 'esptool.py --port /dev/ttyUSB0 erase_flash'
	@echo 'esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 image.bin'
