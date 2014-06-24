package com.hpps.danger;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.support.v7.app.ActionBarActivity;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CompoundButton;
import android.widget.CompoundButton.OnCheckedChangeListener;
import android.widget.EditText;
import android.widget.ToggleButton;

import com.hpps.danger.buildingmanager.ManagerNotificationService;
import com.hpps.danger.buildingmanager.R;
import com.hpps.danger.user.UserNotificationService;

public class Configuration extends ActionBarActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_configuration);

		if (savedInstanceState == null) {
			getSupportFragmentManager().beginTransaction()
			.add(R.id.container, new PlaceholderFragment()).commit();
		}
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {

		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.configuration, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}

	/**
	 * A placeholder fragment containing a simple view.
	 */
	public static class PlaceholderFragment extends Fragment {

		public PlaceholderFragment() {
		}

		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container,
				Bundle savedInstanceState) {
			View rootView = inflater.inflate(R.layout.fragment_configuration,
					container, false);

			ToggleButton managerServiceToggle = (ToggleButton) rootView.findViewById(R.id.managerServiceToggleButton);
			managerServiceToggle.setChecked(ManagerNotificationService.isStarted);

			ToggleButton userServiceToggle = (ToggleButton) rootView.findViewById(R.id.userServiceToggleButton);
			userServiceToggle.setChecked(UserNotificationService.isStarted);

			final EditText ipText = (EditText)rootView.findViewById(R.id.ipText);
			DangerApplication.getApp().setIp(ipText.getText().toString());
			
			
			ipText.addTextChangedListener(new TextWatcher(){
				public void afterTextChanged(Editable s) {
					DangerApplication.getApp().setIp(s.toString());
				}
				public void beforeTextChanged(CharSequence s, int start, int count, int after){}
				public void onTextChanged(CharSequence s, int start, int before, int count){}
			}); 

			managerServiceToggle.setOnCheckedChangeListener(new OnCheckedChangeListener() {

				@Override
				public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
					Intent intent = new Intent(getActivity(), ManagerNotificationService.class);
					if(isChecked) {
						intent.putExtra("ip",ipText.getText() );
						getActivity().startService(intent);
					} else {
						getActivity().stopService(intent);
					}

				}
			});


			userServiceToggle.setOnCheckedChangeListener(new OnCheckedChangeListener() {

				@Override
				public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
					Intent intent = new Intent(getActivity(), UserNotificationService.class);
					if(isChecked) {
						getActivity().startService(intent);
					} else {
						getActivity().stopService(intent);
					}

				}
			});


			return rootView;
		}
	}

}
