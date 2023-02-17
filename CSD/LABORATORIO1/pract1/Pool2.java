// CSD feb 2015 Juansa Sendra

public class Pool2 extends Pool{ //max kids/instructor
    int nI = 0;
    int nK = 0;
    int mki = 2;
    public void init(int ki, int cap) {
        mki = ki;
    }
    public synchronized void kidSwims() throws InterruptedException {
        while (nI == 0 || nK >= mki * nI) {
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
    public synchronized void instructorSwims() {
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