SRCS = inszt_Cashregister.c inszt_Main.c inszt_Productdatabase.c inszt_Specialoffer.c inszt_Userinterface.c 
OBJS = inszt_Cashregister.o inszt_Main.o inszt_Productdatabase.o inszt_Specialoffer.o inszt_Userinterface.o 
DEPS = Cashregister.d Main.d Productdatabase.d Specialoffer.d Userinterface.d 

ifdef ComSpec
	RM = del
else
	RM = rm
endif

all: Cashregister.exe

Cashregister.exe: $(OBJS)
	@echo 'Building target: $@'
	gcc -o Cashregister.exe $(OBJS)
	@echo 'Finished building target: $@'
	@echo ' '

clean:
	$(RM) $(OBJS) $(DEPS) *.exh Cashregister.exe


%.o: %.c
	@echo 'Building file: $<'
	gcc -O0 -g3 -W -I. -I../Src -DMinGW -DTUTORIAL -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
