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

#include <cstdlib>
#include "animation.h"
#include "blinkytile.h"



static uint32_t from_be32(uint8_t *b) {
    return (b[0] << 24) | (b[1] << 16) | (b[2] << 8) | b[3];
}

uint32_t DefaultAnimation::getFrameCount() const {
    return 12;
}

uint32_t DefaultAnimation::getSpeed() const {
    return 100;
}


void DefaultAnimation::getFrame(uint32_t frame, uint8_t *buffer) {
        
    for (int i = 0; i < LED_COUNT; ++i) {
        buffer[3*i] = 255;
        buffer[3*i + 1] = 255;
        buffer[3*i + 2] = 255;
        
    }
}

uint32_t WholeFadeAnimation::getFrameCount() const {
    return 100;
}

uint32_t WholeFadeAnimation::getSpeed() const {
    return 100;
}

WholeFadeAnimation::WholeFadeAnimation(){
    start_randr = rand() % 256;
    start_randb = rand() % 256;
    start_randg = rand() % 256;
    
    end_randr = rand() % 256;
    end_randb = rand() % 256;
    end_randg = rand() % 256;
    
}

void WholeFadeAnimation::getFrame(uint32_t frame, uint8_t *buffer) {
        
    if (frame == 0){
        start_randr = end_randr;
        start_randb = end_randb;
        start_randg = end_randg;
        
        end_randr = rand() % 256;
        end_randb = rand() % 256;
        end_randg = rand() % 256;

    }
    
    for (int i = 0; i < LED_COUNT; ++i) {
        buffer[3*i] = (int)(start_randr*(100 - frame)/100 + end_randr*frame/100);
        buffer[3*i + 1] = (int)(start_randb*(100 - frame)/100 + end_randb*frame/100);
        buffer[3*i + 2] = (int)(start_randg*(100 - frame)/100 + end_randg*frame/100);
        
    }
}

uint32_t PointChangeAnimation::getFrameCount() const {
    return (LED_COUNT*2)+2;
}

uint32_t PointChangeAnimation::getSpeed() const {
    return 300;
}

PointChangeAnimation::PointChangeAnimation(){
    start_randr = rand() % 256;
    start_randb = rand() % 256;
    start_randg = rand() % 256;
    
    end_randr = rand() % 256;
    end_randb = rand() % 256;
    end_randg = rand() % 256;
        
    lednum = rand()%LED_COUNT;
}

void PointChangeAnimation::getFrame(uint32_t frame, uint8_t *buffer) {
        
    if (frame == 0){
        start_randr = end_randr;
        start_randb = end_randb;
        start_randg = end_randg;
        
        end_randr = rand() % 256;
        end_randb = rand() % 256;
        end_randg = rand() % 256;
        
        lednum = rand()%LED_COUNT;
    }
    

        
    for (int i = 0; i < LED_COUNT; ++i) {

        uint32_t x = i;
        
        x = x + LED_COUNT;
        
        if (x < frame){
            x = 0;
        } else {
            x = x - frame;
        }
        
        if (x > LED_COUNT){
            x = LED_COUNT;
        }
        
        buffer[3*i] = start_randr*x/LED_COUNT + end_randr*(LED_COUNT-x)/LED_COUNT;
        buffer[3*i + 1] = start_randb*x/LED_COUNT + end_randb*(LED_COUNT-x)/LED_COUNT;
        buffer[3*i + 2] = start_randg*x/LED_COUNT + end_randg*(LED_COUNT-x)/LED_COUNT;
        
    }
}

void ImageAnimation::init(NoFatStorage& storage_, uint32_t fileNumber_) {
    storage = &storage_;
    fileNumber = fileNumber_;

    uint8_t buffer[ANIMATION_HEADER_LENGTH];
    storage->readFromFile(fileNumber, 0, buffer, ANIMATION_HEADER_LENGTH);

    ledCount = from_be32(&buffer[0]);
    frameCount = from_be32(&buffer[4]);
    speed = from_be32(&buffer[8]);
    type = from_be32(&buffer[12]);

    // TODO: Sanity check the values
}

void ImageAnimation::getFrame(uint32_t frame, uint8_t* buffer) {
    int readLength = ledCount;
    if(readLength > LED_COUNT)
        readLength = LED_COUNT;

    storage->readFromFile(fileNumber,
                ANIMATION_HEADER_LENGTH + frame*ledCount*BYTES_PER_PIXEL,
                buffer,
                readLength*BYTES_PER_PIXEL
        );
}

void ScriptAnimation::init(NoFatStorage &storage, uint32_t fileNumber) {
    this->storage = &storage;
    this->fileNumber = fileNumber;

    scriptSize = storage.fileSize(fileNumber);
    scriptOffset = 0;
    remainingLoops = 0;
    currentAnimation = nullptr;
}

void ScriptAnimation::getFrame(uint32_t frame, uint8_t *buffer) {
    if (currentAnimation == nullptr || (remainingLoops == 0 && frame == 0)) {
        uint32_t animationNumber;
        do {
            uint8_t buffer[8];
            storage->readFromFile(fileNumber, scriptOffset, buffer, sizeof buffer);
            animationNumber = from_be32(&buffer[0]);
            remainingLoops = from_be32(&buffer[4]);
            if (animationNumber != 0xFFFFFFFF)
                break;
            if (scriptOffset != 0) {
                // Rewind.
                scriptOffset = 0;
                continue;
            }
            // Nothing in the script.
            animationNumber = 0;
            break;
        } while (true);

        scriptOffset += 8;
        if (scriptOffset >= scriptSize)
            scriptOffset = 0;
        if (animationNumber == 0xFFFFFFF0) {
            animationNumber = ARM_DWT_CYCCNT; // kind of random
        }
        if (remainingLoops == 0)
            remainingLoops = 1;
        currentAnimation = Animations::gAnimations.getImageAnimation(animationNumber);
    }

    if (frame == 0 && remainingLoops != 0xFFFFFFFF)
        --remainingLoops;
    currentAnimation->getFrame(frame, buffer);
}

bool Animations::isInitialized() {
    return initialized;
}

void Animations::begin(NoFatStorage& storage_) {
    initialized = false;
    storage = &storage_;

    // Look through the file storage, and make an animation for any animation files
    animationCount = 0;
    scriptCount = 0;

    for(int sector = 0; sector < storage->sectors(); sector++) {
        if(storage->isFile(sector)) {
            switch (storage->fileType(sector)) {
            case FILETYPE_ANIMATION:
                this->animations[animationCount++].init(*storage, sector);
                break;
            case FILETYPE_SCRIPT:
                this->scripts[scriptCount++].init(*storage, sector);
                break;
            }
        }
    }
    
    initialized = true;
}

uint32_t Animations::getCount() {
    if (scriptCount > 0)
        return scriptCount;
    if (animationCount > 0)
        return animationCount;
    return 1; // The default animation.
}

Animation* Animations::getAnimation(uint32_t animation) {
    //if (scriptCount > 0)
    //    return &scripts[animation % scriptCount];
   // if (animationCount > 0)
     //   return &animations[animation % animationCount];
    return &default_animation;
}

Animation* Animations::getImageAnimation(uint32_t animation) {
    if (animationCount > 0)
        return &animations[animation % animationCount];
    return &default_animation;
}

Animations Animations::gAnimations;
