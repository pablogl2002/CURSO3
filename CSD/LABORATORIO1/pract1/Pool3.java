// CSD feb 2015 Juansa Sendra

public class Pool3 extends Pool{ //max capacity
    int nI = 0;
    int nK = 0;
    int mki = 2;
    int mCap = 5;
    public void init(int ki, int cap) {
        mki = ki;
        mCap = cap;
    }
    public synchronized void kidSwims() throws InterruptedException {
        while (nI == 0 || nK >= mki * nI || mCap == nK + nI) {
            log.waitingToSwim();
            wait();
        }
        nK++;
        notifyAll();
        log.swimming();
    }
    public synchronized void kidRests() { 
        nK--;
        notifyAll();
        log.resting();
    }
    public synchronized void instructorSwims() throws InterruptedException {
        while (mCap == nK + nI) {
            log.waitingToSwim();
            wait();
        }
        nI++;
        notifyAll();
        log.swimming();
    }
    public synchronized void instructorRests() throws InterruptedException { 
        while(nK > mki * (nI - 1) && nI > 0) {
            log.waitingToRest();
            wait();
        }
        nI--;
        notifyAll();
        log.resting();
    }
}
