package com.danger.utilities;

import android.content.Context;
import android.util.Log;

public class Run {
	
	private static Run run = null;
	private int steps = 0;
	private boolean isRunning = false;
	
	private Run() {
		
	}

	public static Run getInstance() {
		if(run == null) {
			run = new Run();
		}
		return run;
	}
	
	public boolean checkRunning(Context c) {
		int oldSteps = steps;
		steps = Pedometer.getInstance(c).getSteps();
		isRunning = (steps - oldSteps) > 3 ? true : false;
		
		Log.d("debug", "diff = " + (steps-oldSteps) + " CURRENT: " + steps);
		
		return isRunning;
	}
	
	public boolean isRunning() {
		return isRunning;
	}
}
