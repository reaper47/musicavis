import { Howl } from 'howler';


class Timer {
    constructor(elements, interval, timesUpFunc, errorFunc = null) {
        this.workFunc = this._updateTimer;
        this.interval = interval;
        this.errorFunc = errorFunc;
        this.timesUpFunc = timesUpFunc;
        this.timeComponents = {hour: elements.hour, minutes: elements.minutes, seconds: elements.seconds};
        this.sound = new Howl({src: '/static/sounds/sos.mp3', loop: true});
    }

    start(time) {
        this.time = time;
        this.originalTime = time;
        this.expected = Date.now() + this.interval;
        this.timeout = setTimeout(this.step.bind(this), this.interval);
        this.workFunc();
    }

    stop() {
        clearTimeout(this.timeout);
        this._restoreTime();
        this.sound.stop();
    }

    step() {
        if (this.time == 0) {
            this.sound.play();
            this.timesUpFunc();
            return;
        }

        const drift = Date.now() - this.expected;
        if (this.errorFunc && drift > this.interval)
            this.errorFunc();

        this.time--;
        this.workFunc();
        this.expected += this.interval;
        this.timeout = setTimeout(this.step.bind(this), Math.max(0, this.interval - drift));
    }

    _updateTimer() {
        const remainingTime = this._separateTime(this.time);
        this._updateTimeComponents(remainingTime);
    }

    _restoreTime() {
        const remainingTime = this._separateTime(this.originalTime);
        this._updateTimeComponents(remainingTime);
    }

    _separateTime(time) {
        const hours = Math.floor(time/3600);
        const numSecondsHours = hours*3600;
        const minutes = Math.floor(Math.abs(numSecondsHours - time)/60);
        const seconds = time - numSecondsHours - minutes*60;
        return {hours, minutes, seconds};
    }

    _updateTimeComponents(timeStruct) {
        this.timeComponents.hour.textContent = timeStruct.hours;
        this.timeComponents.minutes.textContent = timeStruct.minutes;
        this.timeComponents.seconds.textContent = timeStruct.seconds;
    }
}


class Metronome {
    constructor() {
        this._ctx = new AudioContext();
        this._soundBeatOne = new Howl({src: '/static/sounds/one.wav'});
        this._soundBeatOther = new Howl({src: '/static/sounds/other.wav'});
        this._soundBeatBetween = new Howl({src: '/static/sounds/between.wav'});

        this._lastBar = 0;
        this._lastBeat = 0;

        this._metronome = window.MusicalTimer(() => {
            if (this._ctx.state !== 'running')
                this._ctx.resume();

            if (this._lastBar !== this._metronome.bar) {
                this._lastBar = this._metronome.bar;
                this._beep(this._soundBeatOne);
            }

            if (this._lastBeat !== this._metronome.beat){
                this._lastBeat = this._metronome.beat;
                this._beep(this._soundBeatBetween);
            } else {
                this._beep(this._soundBeatOther);
            }
        });
    }

    _beep(sound) {
        sound.play();

        try {
            this._signatureVisual.children[this._metronome.beat - 2].classList.remove('highlightBeat');
            this._signatureVisual.children[this._metronome.beat - 2].classList.remove('highlightBeat1');
            this._signatureVisual.children[this._metronome.beat - 1].classList.add('highlightBeat');
        } catch (e) {
            this._signatureVisual.lastElementChild.classList.remove('highlightBeat');
            this._signatureVisual.children[this._metronome.beat - 1].classList.add('highlightBeat1');
        }

        this._barNumberElement.value = this._metronome.bar;
    }

    play() {
        this._metronome.play();
    }

    pause() {
        this._metronome.pause();
    }

    stop() {
        try {
            this._signatureVisual.children[this._metronome.beat - 1].classList.remove('highlightBeat');
            this._signatureVisual.children[this._metronome.beat - 1].classList.remove('highlightBeat1');
        } finally {
            this._barNumberElement.value = 1;
            this._metronome.stop();
        }
    }

    setTempo(tempo) {
        this._metronome.tempo = tempo;
    }

    setSignature(signature) {
        this._metronome.signature = signature;
    }

    setSignatureVisual(element) {
        this._signatureVisual = element;
    }

    setSubdivision(subdivision) {
        this._metronome.resolutionFactor = subdivision;
    }

    setBarNumberElement(element) {
        this._barNumberElement = element;
    }
}

export { Timer, Metronome }
