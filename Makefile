# Port can be defined globally but defaults to ttyUSB0
PORT ?= ttyUSB0

.PHONY: shell install_sleep install_multicast

shell:
	mpfshell -o ${PORT}


install_multicast: install_sleep
	mpfshell -o ${PORT} -n -c "put scripts/moisture/boot.py boot.py"
	mpfshell -o ${PORT} -n -c "put scripts/moisture/controller.py controller.py"
	mpfshell -o ${PORT} -n -c "put scripts/weather/with_multicast.py main.py"


install_sleep:
	mpfshell -o ${PORT} -n -c "put scripts/weather/sleep.py sleep.py"


install_moisture:
	mpfshell -o ${PORT} -n -c "put scripts/moisture/boot.py boot.py"
	mpfshell -o ${PORT} -n -c "put scripts/moisture/controller.py controller.py"
	mpfshell -o ${PORT} -n -c "put scripts/moisture/read_moisture.py main.py"

flash:
	@echo "Run this:"
	@echo 'esptool.py --port /dev/ttyUSB0 erase_flash'
	@echo 'esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 image.bin'
