package com.danger.user;

import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.util.HashMap;
import java.util.Map;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.HttpContext;

import android.annotation.SuppressLint;
import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.PowerManager;
import android.os.StrictMode;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.danger.utilities.Pedometer;
import com.danger.utilities.RestUtils;
import com.danger.utilities.Run;
import com.google.gson.GsonBuilder;

@SuppressLint("NewApi")
public class MainActivity extends Activity {

	private String URL =  "http://192.168.1.136";
	protected static final String TAG = "REST";
	private Button button, button2;
	private Handler mHandler = new Handler();

	private PowerManager.WakeLock wl;
	private Button connectionButton;


	@TargetApi(Build.VERSION_CODES.GINGERBREAD)
	@SuppressLint("NewApi")
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.fragment_main);

		addListenerOnButton();

		StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
		StrictMode.setThreadPolicy(policy);


		PowerManager pm = (PowerManager)getSystemService(Context.POWER_SERVICE);
		wl = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "pedometer_wakelock");
		wl.acquire();

		new PedometerThread().execute();

		new Thread(new Runnable() {
			@Override
			public void run() {

				runThread();


			}
		}).start();

	}

	@Override
	protected void onDestroy() {
		// TODO Auto-generated method stub
		super.onDestroy();
		wl.release();
	}

	private void runThread() {
		final Run run = Run.getInstance();

		for(;;) {

			String state = run.checkRunning(MainActivity.this) ? "running" : "quiet";
			HTTPPost(state);


			mHandler.post(new Runnable() {

				@Override
				public void run() {
					((TextView) findViewById(R.id.state)).setText(run.isRunning() ? "running" : "quiet");
					//HTTPPost(state);
				}
			});



			try {
				Thread.sleep(2000);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		}

	}

	public void addListenerOnButton() {

		//Select a specific button to bundle it with the action you want
		button = (Button) findViewById(R.id.button1);

		button.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View view) {
				getURL();

				HTTPPost("running");
			}

		});

		button2 = (Button) findViewById(R.id.button2);

		button2.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View view) {
				getURL();


				HTTPPost("quiet");

			}

		});

		connectionButton = (Button) findViewById(R.id.connection_status);

		connectionButton.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View view) {
				if(connectedTo() != null) {
					Toast.makeText(getApplicationContext(), "Connected to " + connectedTo().toString(), Toast.LENGTH_LONG).show();;
				}
				else {
					Toast.makeText(getApplicationContext(), "Not connected", Toast.LENGTH_LONG).show();;
				}

			}
		});


	}



	private void getURL() {
		if(((EditText) findViewById(R.id.editText1)).getText().toString().length() > 0)
			URL = "http://" + ((EditText) findViewById(R.id.editText1)).getText().toString();
		else URL = "http://192.168.1.136";
	}



	/*	public void execute() {
		Map<String, String> comment = new HashMap<String, String>();
		comment.put("user", "andre");
		comment.put("building", "DEI");
		comment.put("room", "27");
		String json = new GsonBuilder().create().toJson(comment, Map.class);
		makeRequest("http://192.168.1.136:2560/api/notify_run", json);
		Toast toast = Toast.makeText(getApplicationContext(), "Notify Sent!", Toast.LENGTH_SHORT);
		toast.show();
	}

	public static HttpResponse makeRequest(String uri, String json) {
		try {
			HttpPost httpPost = new HttpPost(uri);
			httpPost.setEntity(new StringEntity(json));
			httpPost.setHeader("Accept", "application/json");
			httpPost.setHeader("Content-type", "application/json");
			return new DefaultHttpClient().execute(httpPost);
		} catch (UnsupportedEncodingException e) {
			e.printStackTrace();
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}

	protected String doInBackground(Void... params) {
		HttpClient httpClient = new DefaultHttpClient();
		HttpContext localContext = new BasicHttpContext();
		HttpGet httpGet = new HttpGet("http://192.168.1.136:2560/api/notify_run");
		String text = null;
		try {
			HttpResponse response = httpClient.execute(httpGet, localContext);


			HttpEntity entity = response.getEntity();


			text = getASCIIContentFromEntity(entity);


		} catch (Exception e) {
			return e.getLocalizedMessage();
		}


		return text;
	}

	protected String getASCIIContentFromEntity(HttpEntity entity) throws IllegalStateException, IOException {
		InputStream in = entity.getContent();


		StringBuffer out = new StringBuffer();
		int n = 1;
		while (n>0) {
			byte[] b = new byte[4096];
			n =  in.read(b);


			if (n>0) out.append(new String(b, 0, n));
		}


		return out.toString();
	}


	 */

	private void HTTPPost(String state) {
		final Map<String,String> paramz = new HashMap<String,String>();
		paramz.put("user", "andre");
		paramz.put("state", state);
		paramz.put("building", "DEI");
		paramz.put("room", "10");


		new Thread(new Runnable() {
			@Override
			public void run() {

				RestUtils.doRESTRequest(URL, "2560", "POST", "/api/notify_run", paramz);


			}
		}).start();
	}

	private NetworkInfo connectedTo() {
		ConnectivityManager connectivityManager 
		= (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
		NetworkInfo activeNetworkInfo = connectivityManager.getActiveNetworkInfo();
		if(activeNetworkInfo != null && activeNetworkInfo.isConnected()) {
			return activeNetworkInfo;
		}
		return null;
	}



	private class PedometerThread extends AsyncTask<Void, Integer, Void> {

		@Override
		protected Void doInBackground(Void... arg0) {
			Pedometer pedometer = Pedometer.getInstance(MainActivity.this);

			pedometer.init();

			for(;;) {
				pedometer.start();
				publishProgress(pedometer.getSteps());

			}
		}

		@Override
		protected void onProgressUpdate(Integer... values) {
			((TextView) findViewById(R.id.steps)).setText(values[0].toString());
			//			((TextView) findViewById(R.id.Y)).setText(values[1].toString());
			//			((TextView) findViewById(R.id.Z)).setText(values[2].toString());
		}

	}






}
