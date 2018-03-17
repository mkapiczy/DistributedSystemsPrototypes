package main;
import java.util.Date;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import DelayReq.DelayRequestPublisher;
import DelayResponse.DelayResponse;
import DelayResponse.DelayResponseEventListener;
import DelayResponse.DelayResponsePublisher;
import DelayResponse.DelayResponseSubscriber;
import Sync.Sync;
import Sync.SyncEventListener;
import Sync.SyncPublisher;
import Sync.SyncSubscriber;

public class SlaveMain implements SyncEventListener, DelayResponseEventListener {
	private static long timestamp = 0;
	private static DelayRequestPublisher delayReqPub;
	private static SyncSubscriber syncSub;
	private static DelayResponseSubscriber delayResSub;
	
	private long ts1, tm1, ts2, tm2, offset = 0; //Timestamp for slave and master, used to calculate delay
	
	public static void main(String[] args) {
		//Publishers
		delayReqPub = new DelayRequestPublisher();
		
		//Subscribers
		syncSub = new SyncSubscriber();
		delayResSub = new DelayResponseSubscriber();
		
		startLocalClock();
		
		//Subscribe to synchronization messages
		SlaveMain self = new SlaveMain();
		new Thread(new Runnable() {
		     public void run() {
		    	 syncSub.subscriberMain(0, 0, self);
		     }
		}).start();
		
		//Subscribe to responses delayRequests
		new Thread(new Runnable() {
		     public void run() {
		    	 delayResSub.subscriberMain(0, 0, self);
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
        }, 0, 1100, TimeUnit.MILLISECONDS); //Adding drift to clock
	}


	@Override
	public void newSyncMsg(Sync syncMsg) {
		System.out.println("Sync received, updating timestamp");
		//Set timestamp
		timestamp = syncMsg.timestamp + offset;
		ts1 = timestamp;
		tm1 = syncMsg.timestamp;
		new Thread(new Runnable() {
		     public void run() {
		    	 	delayReqPub.publisherMain(0, 2); //For some reason, if choosing 1, master don't receive the message.
		     }
		}).start();	
		
	}


	@Override
	public void newDelayResMsg(DelayResponse responseMsg) {
		System.out.println("Delay response received, updating offset");
		ts2 = timestamp;
		tm2 = responseMsg.masterTimeStamp;
		
		//Adjust time according to master + delay
		long delay = (ts1 - tm1) + (tm2-ts2) / 2;
		offset = ts1-tm1 - delay;
	}
	
	
}
