package com.danger.utilities;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

public class Pedometer implements SensorEventListener{
	
	private SensorManager sensorManager;

	public static final int FILTER_SIZE = 4;           // shift-register dimension for digital filter
	public static final int NOISE_FRACTION = 10;       // experimental value to ignore HF noise. It represents the fraction of the greatest |max-min|
	public static final int MAX_STEPS_PER_SECOND = 5;
	public static final double MIN_STEPS_PER_SECOND = 0.5;
	public static final int FREQ = 50;                 // in Hz
	public static final int X = 0;
	public static final int Y = 1;
	public static final int Z = 2;


	int MIN_INTERVAL = FREQ/MAX_STEPS_PER_SECOND;
	double MAX_INTERVAL = FREQ/MIN_STEPS_PER_SECOND;

	int[] max_candidate = new int[3];
	int[] min_candidate = new int[3];
	int[] max_value = new int[3];
	int[] min_value = new int[3];
	int[] threshold = new int[3];
	boolean[] active = new boolean[3];                 // active axis

	int[] result = new int[3];                  // new values
	int[][] old = new int[FILTER_SIZE-1][3];      // old values shift register
	float[] temp = new float[3];

	int samples = 0;                // number of samples acquired
	int interval = 0;               // interval between a step and the next one
	volatile int steps = 0;

	int most_active = -1;           // indicates the most active axis
	int buffer_filling = 0;         // used for the first three steps of the digital filtering
	int noise = 0;                  // quantity of noise to be overcame for filtering purposes




	/**
	 * PRIVATE METHODS 
	 */

	/*
	 * Private constructor
	 */
	private Pedometer(Context c) {
		sensorManager = (SensorManager) c.getSystemService(Context.SENSOR_SERVICE);
		sensorManager.registerListener(this, sensorManager.getDefaultSensor( Sensor.TYPE_ACCELEROMETER ),SensorManager.SENSOR_DELAY_NORMAL );
	}

	public void init() {

		for(int i = 0; i < 3; i++) {
			max_candidate[i] = -1000000;
			min_candidate[i] = 1000000;
			max_value[i] = 0;
			min_value[i] = 0;
			threshold[i] = 0;
			active[i] = false;
			result[i] = 0;

			old[i][X] = 0;
			old[i][Y] = 0;
			old[i][Z] = 0;
		}
	}

	// Mobile mean on FITER_PRECISION sample
	void digital_filtering() {

		if(buffer_filling < FILTER_SIZE) {                  // Manage the first three iterations 
			buffer_filling++;                               // using only the filled buffer cells
		}

		for(int i = 0; i < 3; i++) {
			int sum = result[i];
			for(int j = 0; j < buffer_filling-1; j++) {
				sum += old[j][i];
			}
			result[i] = sum/buffer_filling;
		}
	}

	// Manage the election of max and min for the next 50 samples
	void min_max_election() {
		for(int i = 0; i < 3; i++) {

			if(result[i] > max_candidate[i]) {
				max_candidate[i] = result[i];
			}
			if(result[i] < min_candidate[i]) {
				min_candidate[i] = result[i];
			}
		}
	}

	// Define the precision to be overcame in order to ignore High-Frequency Noise
	void dinamic_precision_setting() {
		int current = 0;

		// Calculate the max{ |Xmax-Xmin|, |Ymax-Ymin|, |Zmax, Zmin| }
		for(int i = 0; i < 3; i++) {
			if( Math.abs(max_value[i] - min_value[i]) > current) {
				current = Math.abs(max_value[i] - min_value[i]);
			}
		}

		noise = current/NOISE_FRACTION;
	}


	// Manage the update of max, min and threshold
	void threshold_update() {
		samples = 0;

		for(int i = 0; i < 3; i++) {
			max_value[i] = max_candidate[i];
			min_value[i] = min_candidate[i];

			threshold[i] = (max_value[i] + min_value[i])/2;

			int change = min_candidate[i];
			min_candidate[i] = max_candidate[i];
			max_candidate[i] = change;

			dinamic_precision_setting();
		}
	}

	// Updates the shift register used for digital filter
	void shift_register_update() {
		for(int i = 0; i < 3; i++) {
			old[2][i] = old[1][i];
			old[1][i] = old[0][i];
			old[0][i] = result[i];
		}
	}

	// Acquires the X,Y,Z axis values from accelerometer
	void get_accelerations() {
//		temp[X] = lis302dl.getX();
//		temp[Y] = lis302dl.getY();
//		temp[Z] = lis302dl.getZ();

		for(int i = 0; i < 3; i++) {

			if( Math.abs(result[i] - temp[i]) > noise ) {
				result[i] = (int)temp[i];
				active[i] = true;
			}
		}
	}

	// Recognize the biggest difference of acceleration among the three axis
	void most_active_axis_detection() {
		if(active[X] &&
				Math.abs(result[X] - old[0][X]) >= Math.abs(result[Y] - old[0][Y]) &&
				Math.abs(result[X] - old[0][X]) >= Math.abs(result[Z] - old[0][Z])) {
			most_active = X;
		}
		else if(active[Y] &&
				Math.abs(result[Y] - old[0][Y]) >= Math.abs(result[X] - old[0][X]) &&
				Math.abs(result[Y] - old[0][Y]) >= Math.abs(result[Z] - old[0][Z])) {
			most_active = Y;
		}
		else if(active[Z] &&
				Math.abs(result[Z] - old[0][Z]) >= Math.abs(result[Y] - old[0][Y]) &&
				Math.abs(result[Z] - old[0][Z]) >= Math.abs(result[X] - old[0][X])) {
			most_active = Z;
		}
		else {
			most_active = -1;
		}

		for(int i = 0; i < 3; i++) {
			active[i] = false;
		}

	} 

	// Implements the step recognition logic
	void step_recognition() {
		if(0 <= most_active && most_active <= 2) {
			if(old[0][most_active] > threshold[most_active] &&
					threshold[most_active] > result[most_active]) {                  // recognize a negative slope threshold cross
				if (interval >= MIN_INTERVAL) {                                 // ignore steps faster than one every 200ms
					if(interval <= MAX_INTERVAL)  {                                     // ignore steps slower than one every 2s
						steps++;     
					}
				}
				interval = 0;
			}
		}
	}

	private static Pedometer pPedometer = null;

	/** 
	 * PUBLIC METHODS
	 */

	public static synchronized Pedometer getInstance(Context c) {
		if(pPedometer == null) {
			pPedometer = new Pedometer(c);
		}
		return pPedometer;
	}  


	public void start() {           


		digital_filtering();
		min_max_election();

		if(samples == 10) {
			threshold_update();
		}

		shift_register_update();
		get_accelerations();
		most_active_axis_detection();
		step_recognition();

		interval++;
		samples++;

		/*printf("X: %i\n", result[X]);
	        printf("X_T: %i\n", threshold[X]);
	        printf("Y: %i\n", result[Y]);
	        printf("Y_T: %i\n", threshold[Y]);
	        printf("Z: %i\n", result[Z]);
	        printf("Z_T: %i\n\n", threshold[Z]);
	        printf("S: %d\n\n\n", steps);
		 */

		try {
			Thread.sleep((int)((1f/FREQ) * 1000) /*+ 64*0.520*/);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}    
	}



	synchronized public int getSteps() {
		return steps;
	}

	@Override
	public void onAccuracyChanged(Sensor sensor, int accuracy) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void onSensorChanged(SensorEvent event) {
		 if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {	
			             updateValues(event);
		 }

	}
	
	private void updateValues(SensorEvent event) {
		temp = event.values;
	}
	
	public float[] getAcc() {
		return temp;
	}


}
