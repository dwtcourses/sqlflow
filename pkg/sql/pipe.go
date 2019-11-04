// Copyright 2019 The SQLFlow Authors. All rights reserved.
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package sql

import (
	"errors"
)

// ErrClosedPipe will occur when manipulating an already closed pipe
var ErrClosedPipe = errors.New("pipe: write on closed pipe")

// pipe follows the design at https://blog.golang.org/pipelines
// - wrCh: chan for piping data
// - done: chan for signaling Close from Reader to Writer
type pipe struct {
	wrCh chan interface{}
	done chan struct{}
}

// PipeReader reads real data
type PipeReader struct {
	p *pipe
}

// PipeWriter writes real data
type PipeWriter struct {
	p *pipe
}

// Pipe creates a synchronous in-memory pipe.
//
// It is safe to call Read and Write in parallel with each other or with Close.
// Parallel calls to Read and parallel calls to Write are also safe:
// the individual calls will be gated sequentially.
func Pipe() (*PipeReader, *PipeWriter) {
	p := &pipe{
		wrCh: make(chan interface{}),
		done: make(chan struct{})}
	return &PipeReader{p}, &PipeWriter{p}
}

// Close closes the reader; subsequent writes to the
func (r *PipeReader) Close() {
	close(r.p.done)
}

// ReadAll returns the data chan. The caller should
// use it as `for r := range pr.ReadAll()`
func (r *PipeReader) ReadAll() chan interface{} {
	return r.p.wrCh
}

// Close closes the writer; subsequent ReadAll from the
// read half of the pipe will return a closed channel.
func (w *PipeWriter) Close() {
	close(w.p.wrCh)
}

// Write writes the item to the underlying data stream.
// It returns ErrClosedPipe when the data stream is closed.
func (w *PipeWriter) Write(item interface{}) error {
	select {
	case w.p.wrCh <- item:
		return nil
	case <-w.p.done:
		return ErrClosedPipe
	}
}
