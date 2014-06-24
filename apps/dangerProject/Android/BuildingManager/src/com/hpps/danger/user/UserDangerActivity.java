package com.hpps.danger.user;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.StatusLine;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;

import com.hpps.danger.buildingmanager.R;
import com.hpps.danger.buildingmanager.util.SystemUiHider;

/**
 */
public class UserDangerActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);


		setContentView(R.layout.user_activity_danger);

		TextView buildingText = (TextView)findViewById(R.id.building_text);
		TextView roomText = (TextView)findViewById(R.id.room_text);
		TextView descriptionText = (TextView)findViewById(R.id.danger_text);

		if(getIntent().hasExtra("building")){
			buildingText.setText("Building: " + getIntent().getExtras().getString("building"));
			roomText.setText("CSE: " + getIntent().getExtras().getString("room"));
			descriptionText.setText("Description: " + getIntent().getExtras().getString("description"));
		}



	}



}
