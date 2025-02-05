import json
import sys
import os


def get_root(body) :
    for part in body["part"] :
        if part["root"] :
            return part    

def get_part(id_, body) :
    for part in body["part"] :
        if part["id"] == id_ :
            return part

#def fix_param(val) :
#    return round(val * 10000)/10000.0


def write_part(output, part, body, indentation_level=0) :
    for _ in range(indentation_level) :
        output.write("\t")
    if part["root"] :
        output.write("0")
    else :
        for connection in body["connection"] :
            if connection["dest"] == part["id"] :
                # need to fix slot numbering
                # see lines 182-186 in PartRepresentation
                if get_part(connection["src"], 
                            body)["type"] == "CoreComponent": 
                    output.write(str(connection["srcSlot"]))
                elif get_part(connection["src"], 
                            body)["type"] == "CoreComponentNoIMU": 
                    output.write(str(connection["srcSlot"]))
                else :
                    output.write(str(connection["srcSlot"]-1))
    output.write(" ")
    output.write(part["type"])
    output.write(" ")
    output.write(str(part["id"]))
    output.write(" ")
    output.write(str(part["orientation"]))
    if "evolvableParam" in part :
        for param in part["evolvableParam"] :
            output.write(" ")
            output.write(str(round(param["paramValue"],8)))
    output.write("\n")
    if "connection" in body :
        for connection in body["connection"] :
            if connection["src"] == part["id"] :            
                write_part(output, get_part(connection["dest"], body), 
                           body, indentation_level+1)

def write_body(output, body):
    write_part(output, get_root(body), body)
        
def write_brain(output, brain):

    # first need to write add-hidden-neuron lines
    if "neuron" in brain :
        for neuron in brain["neuron"] :
            if neuron["layer"] == "hidden" :
                output.write(neuron["bodyPartId"])
                output.write(" ")
                output.write(neuron["type"])
                output.write("\n")
    output.write("\n")

    # then connection weights
    if "connection" in brain:
        for connection in brain["connection"] :
            output.write(connection["src"].split("-")[0])
            output.write(" ")
            output.write(connection["src"].split("-")[1])
            output.write(" ")
            output.write(connection["dest"].split("-")[0])
            output.write(" ")
            output.write(connection["dest"].split("-")[1])
            output.write(" ")
            output.write(str(connection["weight"]))
            output.write("\n")
    output.write("\n")
    
    # then params/biases
    if "neuron" in brain :
        for neuron in brain["neuron"] :
            if neuron["layer"] != "input" :
                output.write(neuron["id"].split("-")[0])
                output.write(" ")
                output.write(neuron["id"].split("-")[1])
                output.write(" ")
                if neuron["type"] == "oscillator" :
                    output.write("oscillator ")
                    output.write(str(neuron["period"]))
                    output.write(" ")
                    output.write(str(neuron["phaseOffset"]))
                    output.write(" ")
                    output.write(str(neuron["gain"]))
                else :
                    output.write(str(neuron["bias"]))
                output.write("\n")
        
if __name__ == "__main__":

	dir_path = os.path.dirname(os.path.realpath(__file__))
	dlist = os.listdir(dir_path)
	for dir in dlist:
		if os.path.isdir(dir):
			current_dir_path = os.path.join(dir_path, dir)
			file_name = 'GenerationBest-37.json'
			file = os.path.join(current_dir_path, file_name)
			if os.path.exists(file):
				print("File %s found in dir %s." %(file_name, current_dir_path))
				out_file = os.path.join(current_dir_path, 'robot.txt')
				robot = json.load(open(file,"r"))
				output = open(out_file, "w")
				write_body(output, robot["body"])    
				output.write("\n") 
				if "brain" in robot :
					write_brain(output, robot["brain"])
    
    

