/*
 * LED Animation loader/player
 * 
 * Copyright (c) 2014 Matt Mets
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#ifndef ANIMATION_H
#define ANIMATION_H

#include "nofatstorage.h"

#define ANIMATION_HEADER_LENGTH 16

// Max. number of animations that can be read from the flash (arbitrary)
#define MAX_ANIMATIONS_COUNT 100
#define MAX_SCRIPTS_COUNT 10

class Animation {
  public:
    ~Animation() {}

    // Retrieve the animation data for the given frame
    // Reads LED_COUT*BYTES_PER_PIXEL of data.
    // @param frame Animation frame
    // @param buffer Buffer to write the data to
    virtual void getFrame(uint32_t frame, uint8_t* buffer) = 0;
    virtual uint32_t getFrameCount() const = 0;
    virtual uint32_t getSpeed() const = 0; 
};

class ImageAnimation : public Animation {
  private:
    NoFatStorage* storage;       // Storage container to read from
    uint32_t fileNumber;         // File number containing this animation
    uint32_t ledCount;           // Number of LEDs controlled by this animation
    uint32_t frameCount;         // Number of frames in this animation
    uint32_t speed;              // Speed, in ms between frames
    uint32_t type;               // Type, 0x0000 = BGR uncompressed

    // Initialize the animation using the given file number
    // @param fileNumber File to read from
    void init(NoFatStorage& storage_, uint32_t fileNumber_);

  public:
    ~ImageAnimation() {}
    void getFrame(uint32_t frame, uint8_t* buffer) override;
    inline uint32_t getFrameCount() const override { return frameCount; }
    inline uint32_t getSpeed() const override { return speed; }

    friend class Animations;
};

class ScriptAnimation : public Animation {
  private:
    NoFatStorage *storage;
    uint32_t fileNumber;
    uint32_t scriptSize;
    uint32_t scriptOffset;
    uint32_t remainingLoops;
    Animation *currentAnimation;

    void init(NoFatStorage &storage, uint32_t fileNumber);
    void loadNextAnimation();
  public:
    ~ScriptAnimation() {}
    void getFrame(uint32_t frame, uint8_t *buffer) override;
    uint32_t getFrameCount() const override {
        return currentAnimation ? currentAnimation->getFrameCount() : 0;
    }
    uint32_t getSpeed() const override {
        return currentAnimation ? currentAnimation->getSpeed() : 100;
    }

    friend class Animations;
};

class DefaultAnimation : public Animation {
public:
    uint32_t getFrameCount() const override;
    uint32_t getSpeed() const override;
    void getFrame(uint32_t frame, uint8_t *buffer) override;
};

class WholeFadeAnimation: public Animation {
public:
    WholeFadeAnimation();
    uint32_t getFrameCount() const override;
    uint32_t getSpeed() const override;
    void getFrame(uint32_t frame, uint8_t *buffer) override;
    
private:
        uint32_t start_randr;
        uint32_t start_randb;
        uint32_t start_randg;
    
        uint32_t end_randr;
        uint32_t end_randb;
        uint32_t end_randg;
    
};

class PointChangeAnimation: public Animation {
public:
    PointChangeAnimation();
    uint32_t getFrameCount() const override;
    uint32_t getSpeed() const override;
    void getFrame(uint32_t frame, uint8_t *buffer) override;
    
private:
    uint32_t start_randr;
    uint32_t start_randb;
    uint32_t start_randg;
    
    uint32_t end_randr;
    uint32_t end_randb;
    uint32_t end_randg;
    
    uint32_t lednum;
    
};

class Animations {
  private:
    NoFatStorage* storage;       // Storage container to read from

    ImageAnimation animations[MAX_ANIMATIONS_COUNT];	// Static table of animations
    ScriptAnimation scripts[MAX_SCRIPTS_COUNT];
    PointChangeAnimation default_animation;
    uint32_t animationCount;    // Number of animations in this class
    uint32_t scriptCount;

    bool initialized;           // True if initialized correctly

  public:
    static Animations gAnimations;
  
    // Initialize the animations table
    // @param storage_ Storage container to read from
    void begin(NoFatStorage& storage_);

    // True if the animations table was read correctly from flash
    bool isInitialized();

    // Read the number of animations stored in the flash
    // @return Number of animations stored in the flash
    uint32_t getCount();

    // Get the requested animation
    Animation* getAnimation(uint32_t animation);

    Animation* getImageAnimation(uint32_t animation);
};

#endif
