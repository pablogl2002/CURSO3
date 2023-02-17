// CSD feb 2013 Juansa Sendra

public class Pool4 extends Pool { //kids cannot enter if there are instructors waiting to exit
    int nI = 0;
    int nK = 0;
    int mki = 2;
    int mCap = 5;
    boolean cond = false;
    
    public void init(int ki, int cap) {
        mki = ki;
        mCap = cap;
    }
    public synchronized void kidSwims() throws InterruptedException {
        while (nI == 0 || nK >= mki * nI || mCap <= nK + nI || cond) {
            log.waitingToSwim();
            wait();
        }
        nK++;
        log.swimming();
        notifyAll();
    }
    public synchronized void kidRests() { 
        nK--;
        log.resting();
        notifyAll();
    }
    public synchronized void instructorSwims() throws InterruptedException {
        while (mCap <= nK + nI) {
            log.waitingToSwim();
            wait();
        }
        nI++;
        log.swimming();
        notifyAll();
    }
    public synchronized void instructorRests() throws InterruptedException { 
        while(nK > mki * (nI - 1)) {
            cond = true;
            log.waitingToRest();
            wait();
        }
        cond = false;
        nI--;
        log.resting();
        notifyAll();
    }
}