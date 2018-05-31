{
    // here we define a variable for record keeping
    distances : [],    
	IR : [],
	current_velocity : [],
	
    // optional function called at the beginning of the simulation
    setupSimulation: function() {
			this.startPos = this.getRobot().getCoreComponent().getRootPosition();
			this.angular_velocity_vals = [];
			this.IR_vals = [];;

			return true    },

    // optional function called after each step of simulation
    afterSimulationStep: function() {
		var sensors = this.getRobot().getSensors();
		var current_IR_val = []
		for (var i = 0; i < sensors.length; i++) {
			if (/Distance$/.test(sensors[i].getLabel())) {
				current_IR_val.push(sensors[i].read())
			}			
		}
		this.IR_vals.push(current_IR_val)
		
		var sensors = this.getRobot().getCoreComponent().getSensors()
		current_velocity_vals = [0, 0, 0, 0, 0, 0];
		for (var i = 0; i < sensors.length; i++){
			sensor = sensors[i]
			if (sensor.getType()=="ImuSensorElement") {
				var label = sensor.getLabel()
				if (/Roll$/.test(label)) {
					current_velocity_vals[0] = sensor.read()
				} else if (/Pitch$/.test(label)) {
					current_velocity_vals[1] = sensor.read()
				} else if (/Yaw$/.test(label)) {
					current_velocity_vals[2] = sensor.read()
				} else if (/x-acceleration$/.test(label)) {
					current_velocity_vals[3] = sensor.read()
				} else if (/y-acceleration$/.test(label)) {
					current_velocity_vals[4] = sensor.read()
				} else if (/z-acceleration$/.test(label)) {
					current_velocity_vals[5] = sensor.read()
				}
			}
		}
		this.angular_velocity_vals.push(current_velocity_vals)
		return true
	},

    // optional function called at the end of the simulation
    endSimulation: function() {

		// Compute robot ending position from its closest part to the origin
		var minDistance = Number.MAX_VALUE;
	        
		bodyParts = this.getRobot().getBodyParts();
		for (var i = 0; i < bodyParts.length; i++) {
			var xDiff = (bodyParts[i].getRootPosition().x - this.startPos.x);
			var yDiff = (bodyParts[i].getRootPosition().y - this.startPos.y);
			var dist = Math.sqrt(Math.pow(xDiff,2) + Math.pow(yDiff,2));
                
			if (dist < minDistance) {
				minDistance = dist;
			}
			this.distances.push(minDistance);
		}
		return true;
    },
    // the one required method... return the fitness!
    // here we return minimum distance travelled across evaluations
    getFitness: function() {
		fitness = this.distances[0];
			for (var i=1; i<this.distances.length; i++) {
			if (this.distances[i] < fitness)
				fitness = this.distances[i];
		}
		IR_penality = 0.0
		for (var i=1; i<this.IR_vals.length; i++){
			max_val = 0.0
			for (var j=1; j<this.IR_vals[i].length; j++){
				if(this.IR_vals[i][j] > max_val){
					max_val = this.IR_vals[i][j]
				}
			}
			if (max_val > IR_penality){
				IR_penality = max_val
			}
		}
		worst_angular_velocity = 0.0
		vibration_speed = 100
		//1600 episodes for 8 seconds, or 200 per seconds
		t0 = 0
		t1 = 0
		penality0 = 0
		penality1 = 0
		direction0 = 0
		direction1 = 0
		for (var i = 0; i < this.angular_velocity_vals.length; i++){
			penality = 0.0
			current = this.angular_velocity_vals[i]
			speed = 0.0
			for (var j = 3; j < current.length; j ++){
				speed += Math.abs(current[j])
			}
			for (var j = 0; j < 3; j++){
				if (current[j] != 0){
					sign = current[j]/(Math.abs(current[j]))
				}else{
					sign = 0
				}
				if(j == 2){
					penality += Math.abs(current[j]) * 0.0
				} else if (j==1){
					if (direction1 == sign){
						penality1 += Math.abs(current[j])
						t1 += 1
					}else{
						penality1 = 0
						t1 = 0
						direction1 = sign
					}
				} else if(j == 0){
					if (direction0 == sign){
						penality0 += Math.abs(current[j])
						t0 += 1
					}else{
						penality0 = 0
						t0 = 0
						direction0 = sign
					}
				}
			}
			if(penality0 * t0 > worst_angular_velocity && t0 > vibration_speed){
				worst_angular_velocity = penality0 * t0// * speed
				//console.log(speed)
			}
			if(penality1 * t1 > worst_angular_velocity && t1 > vibration_speed){
				worst_angular_velocity = penality1 * t1// * speed
				//console.log(speed)
			}
		}
		worst_angular_velocity = worst_angular_velocity * 0.0005
		//IR_penality = IR_penality * 0.5
		IR_penality = 0
		//console.log()
		//console.log(worst_angular_velocity)
		//console.log(fitness)
		//console.log(IR_penality)
		//console.log(this.IR_vals[0])
		//console.log('-------')
		fitness = fitness - worst_angular_velocity - IR_penality;
		if (this.IR_vals[0].length == 0){
			fitness = Math.min(0, -fitness)
		}
		return fitness
	},

}