package main;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import DelayReq.DelayRequest;
import DelayReq.DelayRequestEventListener;
import DelayReq.DelayRequestSubscriber;
import DelayResponse.DelayResponsePublisher;
import Sync.SyncPublisher;

public class MasterMain implements DelayRequestEventListener {
	private static int timestamp = 0;
	private static SyncPublisher syncPub;
	private static DelayResponsePublisher delayResPub;
	private static DelayRequestSubscriber delayReqSub;
	
	private static MasterMain self = new MasterMain();

	public static void main(String[] args) {
		//Publishers
		syncPub = new SyncPublisher();
		delayResPub = new DelayResponsePublisher();
		
		//Subscribers
		delayReqSub = new DelayRequestSubscriber();
		
		startLocalClock();
		
		new Thread(new Runnable() {
		     public void run() {
		    	 	syncPub.publisherMain(0, 0, timestamp);
		     }
		}).start();
		
		new Thread(new Runnable() {
		     public void run() {
		    	 	delayReqSub.subscriberMain(0, 0, self);
		     }
		}).start();

	}

	private static void startLocalClock() {
		final ScheduledExecutorService ses = Executors.newSingleThreadScheduledExecutor();
        ses.scheduleWithFixedDelay(new Runnable() {
            @Override
            public void run() {
            	timestamp += 1;
                System.out.println(timestamp);
            }
        }, 0, 1000, TimeUnit.MILLISECONDS); 
	}
	
	public static int getTimestamp() {
		return timestamp;
	}

	@Override
	public void newDelayReqMsg(DelayRequest reqMsg) {
		System.out.println("Delay request received, sending response");
		new Thread(new Runnable() {
		     public void run() {
		    	 	delayResPub.publisherMain(0, 2, reqMsg.msgId, timestamp);
		     }
		}).start();
	}
}
